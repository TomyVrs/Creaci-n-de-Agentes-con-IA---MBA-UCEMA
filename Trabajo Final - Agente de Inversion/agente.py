"""
Agente de Análisis de Inversión — Trabajo Final
MBA UCEMA · Programación de y con Agentes de IA

Tres rondas encadenadas:
1) investigación inicial con web search;
2) búsqueda dirigida con web search;
3) síntesis/decisión sin búsqueda nueva.

Cada corrida real se guarda de forma reconstruible en corridas/<id>/.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
CORRIDAS_DIR = ROOT / "corridas"
HISTORIAL_PATH = ROOT / "historial.json"
SYSTEM_PROMPT_PATH = ROOT / "prompts" / "system_prompt.md"
USER_PROMPT_PATH = ROOT / "prompts" / "user_prompt.md"

# Precios documentados para Claude Sonnet 4.6, estándar global.
PRICE_INPUT_PER_MTOK = 3.0
PRICE_OUTPUT_PER_MTOK = 15.0
PRICE_WEB_SEARCH = 0.01  # USD 10 / 1.000 búsquedas


def _get_client():
    """Import tardío: permite correr el smoke test sin instalar el SDK."""
    try:
        import anthropic
    except ImportError as exc:
        raise RuntimeError(
            "Falta la dependencia 'anthropic'. Ejecutá: pip install -r requirements.txt"
        ) from exc
    return anthropic.Anthropic()


def _extract_json(raw_text: str) -> dict[str, Any]:
    clean = re.sub(r"```json|```", "", raw_text, flags=re.IGNORECASE).strip()
    start = clean.find("{")
    end = clean.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("La respuesta no contiene un objeto JSON completo.")
    return json.loads(clean[start : end + 1])


def _web_search_count(usage: Any) -> int:
    server = getattr(usage, "server_tool_use", None)
    if server is None:
        return 0
    if isinstance(server, dict):
        return int(server.get("web_search_requests", 0) or 0)
    return int(getattr(server, "web_search_requests", 0) or 0)


def call_claude(prompt: str, max_tokens: int, use_search: bool = True, system: str | None = None):
    """Una llamada real. Devuelve parsed, usage, sources y raw_text."""
    client = _get_client()
    kwargs = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system
    if use_search:
        kwargs["tools"] = [
            {"type": "web_search_20260209", "name": "web_search", "max_uses": 6}
        ]

    resp = client.messages.create(**kwargs)
    text_blocks = [b for b in resp.content if getattr(b, "type", None) == "text"]
    raw_text = "\n".join(getattr(b, "text", "") for b in text_blocks).strip()
    parsed = _extract_json(raw_text)

    sources: list[dict[str, str]] = []
    seen: set[str] = set()
    for block in text_blocks:
        for citation in getattr(block, "citations", None) or []:
            url = getattr(citation, "url", None)
            if url and url not in seen:
                seen.add(url)
                sources.append({
                    "url": url,
                    "title": getattr(citation, "title", None) or url,
                })

    usage = {
        "input_tokens": int(getattr(resp.usage, "input_tokens", 0) or 0),
        "output_tokens": int(getattr(resp.usage, "output_tokens", 0) or 0),
        "web_search_requests": _web_search_count(resp.usage),
    }
    return parsed, usage, sources, raw_text


def _extract_prompt_variant(text: str, variant_number: int) -> str:
    pattern = rf"## Variante {variant_number}[^\n]*\n[\s\S]*?```\s*\n([\s\S]*?)\n```"
    match = re.search(pattern, text)
    if not match:
        raise ValueError(f"No pude leer la Variante {variant_number} de user_prompt.md")
    return match.group(1).strip()


def cargar_variantes_user_prompt() -> dict[int, str]:
    text = USER_PROMPT_PATH.read_text(encoding="utf-8")
    return {i: _extract_prompt_variant(text, i) for i in (1, 2, 3)}


def render(template: str, replacements: dict[str, Any]) -> str:
    result = template
    for key, value in replacements.items():
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        result = result.replace("{" + key + "}", str(value))
    return result


def cargar_historial() -> list[dict[str, Any]]:
    if HISTORIAL_PATH.exists():
        return json.loads(HISTORIAL_PATH.read_text(encoding="utf-8"))
    return []


def calcular_hit_rate(historial: list[dict[str, Any]]) -> str:
    resueltos = [
        h for h in historial
        if h.get("resultado_real") in ("Acertó", "No acertó", "Parcial")
    ]
    if not resueltos:
        return "Todavía no hay veredictos anteriores resueltos para calcular una tasa de acierto real."
    aciertos = sum(1 for h in resueltos if h["resultado_real"] == "Acertó")
    tasa = round(100 * aciertos / len(resueltos))
    return f"Tasa de acierto histórica: {tasa}% sobre {len(resueltos)} veredictos anteriores ya resueltos."


def estimar_costo(usage: dict[str, int]) -> dict[str, float]:
    input_cost = usage["input_tokens"] / 1_000_000 * PRICE_INPUT_PER_MTOK
    output_cost = usage["output_tokens"] / 1_000_000 * PRICE_OUTPUT_PER_MTOK
    search_cost = usage.get("web_search_requests", 0) * PRICE_WEB_SEARCH
    return {
        "tokens_usd": round(input_cost + output_cost, 6),
        "web_search_usd": round(search_cost, 6),
        "total_usd": round(input_cost + output_cost + search_cost, 6),
    }


def analizar(instrumento: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    fecha = now.strftime("%Y-%m-%d")
    system = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    variants = cargar_variantes_user_prompt()

    total_usage = {"input_tokens": 0, "output_tokens": 0, "web_search_requests": 0}
    all_sources: list[dict[str, str]] = []
    rounds: dict[str, Any] = {}

    def run_round(name: str, prompt: str, max_tokens: int, use_search: bool):
        parsed, usage, sources, raw = call_claude(
            prompt, max_tokens=max_tokens, use_search=use_search, system=system
        )
        for k in total_usage:
            total_usage[k] += usage.get(k, 0)
        for source in sources:
            if source["url"] not in {s["url"] for s in all_sources}:
                all_sources.append(source)
        rounds[name] = {
            "prompt": prompt,
            "raw_output": raw,
            "parsed_output": parsed,
            "usage": usage,
            "sources": sources,
        }
        return parsed

    prompt1 = render(variants[1], {"instrumento": instrumento, "fecha": fecha})
    r1 = run_round("ronda1", prompt1, 2200, True)
    print(f"[Ronda 1 OK] precio={r1.get('precioReferencia')}")

    prompt2 = render(variants[2], {
        "instrumento": instrumento,
        "fecha": fecha,
        "evidenciaAFavor_ronda1": r1.get("evidenciaAFavor", []),
        "evidenciaEnContra_ronda1": r1.get("evidenciaEnContra", []),
        "gapsDeInformacion_ronda1": r1.get("gapsDeInformacion", []),
    })
    r2 = run_round("ronda2", prompt2, 2500, True)
    print(f"[Ronda 2 OK] niveles={r2.get('nivelesTecnicos')}")

    historial = cargar_historial()
    hit_rate = calcular_hit_rate(historial)
    evidencia_favor = r1.get("evidenciaAFavor", []) + r2.get("evidenciaAdicionalAFavor", [])
    evidencia_contra = r1.get("evidenciaEnContra", []) + r2.get("evidenciaAdicionalEnContra", [])

    prompt3 = render(variants[3], {
        "instrumento": instrumento,
        "fecha": fecha,
        "precioReferencia": r1.get("precioReferencia", "no disponible"),
        "evidenciaAFavor_combinada": evidencia_favor,
        "evidenciaEnContra_combinada": evidencia_contra,
        "gapsResueltos": r2.get("gapsResueltos", []),
        "nivelesTecnicos": r2.get("nivelesTecnicos", {}),
        "comparable": r2.get("comparable", "no disponible"),
        "tasaLibreRiesgo": r2.get("tasaLibreRiesgo", "no disponible"),
        "hitRateTexto": hit_rate,
    })
    r3 = run_round("ronda3", prompt3, 4500, False)
    print(f"[Ronda 3 OK] veredicto={r3.get('veredicto')} confianza={r3.get('confianza')}")

    salida_final = {**r3, "fuentes": all_sources}
    historial.append({
        "instrumento": instrumento,
        "fecha": fecha,
        "veredicto": r3.get("veredicto"),
        "confianza": r3.get("confianza"),
        "resultado_real": None,
    })
    HISTORIAL_PATH.write_text(json.dumps(historial, indent=2, ensure_ascii=False), encoding="utf-8")

    return {
        "instrumento": instrumento,
        "fecha_corrida": now.isoformat(),
        "modelo": MODEL,
        "entrada": {"instrumento": instrumento, "fecha_referencia": fecha},
        "rondas": rounds,
        "salida_final": salida_final,
        "uso": total_usage,
        "costo_estimado": estimar_costo(total_usage),
    }


def _slug(text: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", text.strip())
    return cleaned.strip("_") or "instrumento"


def guardar_corrida(resultado: dict[str, Any]) -> Path:
    CORRIDAS_DIR.mkdir(exist_ok=True)
    dt = datetime.fromisoformat(resultado["fecha_corrida"])
    run_id = f"corrida_{dt.strftime('%Y%m%d_%H%M%S')}_{_slug(resultado['instrumento'])}"
    run_dir = CORRIDAS_DIR / run_id
    run_dir.mkdir(exist_ok=False)

    (run_dir / "fecha.txt").write_text(resultado["fecha_corrida"] + "\n", encoding="utf-8")
    (run_dir / "entrada.md").write_text(
        f"# Entrada real\n\n- Instrumento: {resultado['instrumento']}\n"
        f"- Fecha de referencia: {resultado['entrada']['fecha_referencia']}\n"
        f"- Modelo: {resultado['modelo']}\n",
        encoding="utf-8",
    )
    (run_dir / "salida.json").write_text(
        json.dumps(resultado["salida_final"], indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (run_dir / "corrida.json").write_text(
        json.dumps(resultado, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    manifest_path = CORRIDAS_DIR / "manifest.json"
    manifest = []
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.append({
        "id": run_id,
        "instrumento": resultado["instrumento"],
        "fecha_corrida": resultado["fecha_corrida"],
        "modelo": resultado["modelo"],
        "veredicto": resultado["salida_final"].get("veredicto"),
        "confianza": resultado["salida_final"].get("confianza"),
        "uso": resultado["uso"],
        "costo_estimado": resultado["costo_estimado"],
        "path": f"corridas/{run_id}/corrida.json",
    })
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return run_dir


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Uso: python agente.py "<instrumento>"')
        sys.exit(1)

    instrumento = sys.argv[1]
    print(f"Analizando: {instrumento}...")
    resultado = analizar(instrumento)
    ruta = guardar_corrida(resultado)
    print(f"\n✓ Corrida guardada en: {ruta}")
    print(f"  Veredicto: {resultado['salida_final'].get('veredicto')} ({resultado['salida_final'].get('confianza')})")
    print(f"  Web searches: {resultado['uso']['web_search_requests']}")
    print(f"  Costo estimado total: USD {resultado['costo_estimado']['total_usd']:.6f}")
