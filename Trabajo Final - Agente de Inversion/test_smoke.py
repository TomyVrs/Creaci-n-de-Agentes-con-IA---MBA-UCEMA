"""Smoke test determinista: valida orquestación, trazabilidad y costos sin API real."""

import json
import shutil
from pathlib import Path
from unittest.mock import patch

import agente

R1 = {
    "precioReferencia": "123.45 USD",
    "evidenciaAFavor": ["Resultado trimestral por encima de lo esperado"],
    "evidenciaEnContra": ["Deuda subió 15% interanual"],
    "gapsDeInformacion": ["¿Nivel de soporte actual?"],
}
R2 = {
    "gapsResueltos": [{"pregunta": "¿Nivel de soporte?", "respuesta": "115 según fuente técnica"}],
    "evidenciaAdicionalAFavor": ["Volumen en alza"],
    "evidenciaAdicionalEnContra": ["Competidor bajó guidance"],
    "nivelesTecnicos": {"zonaEntrada": "118-122", "tomarGanancia": "140", "stopLoss": "110", "soporte": "115", "resistencia": "135"},
    "comparable": "Empresa Comparable SA",
    "tasaLibreRiesgo": "4.8% anual",
}
R3 = {
    "instrumento": "SIMULADO_SMOKE_TEST",
    "precioReferencia": "123.45 USD",
    "evidenciaAFavor": [{"texto": "Resultado trimestral superó lo esperado", "tipo": "Dato"}],
    "evidenciaEnContra": [{"texto": "Deuda subió 15% interanual", "tipo": "Dato"}],
    "resolucion": "La evidencia favorable pesa más en el escenario actual.",
    "varianteCritica": "Cambio regulatorio adverso.",
    "comparacionAlternativas": {"cash": "Supera tasa libre de riesgo.", "alternativa": "Empresa Comparable SA", "comparacion": "Mejor momentum."},
    "veredicto": "Comprar",
    "confianza": "Media",
    "calibracion": "Sin historial resuelto.",
    "autocritica": "La deuda puede deteriorar el caso.",
    "posicionSugerida": "3-5%",
    "horizonteRecomendado": "6-12 meses",
    "zonaEntrada": "118-122",
    "tomarGanancia": "140",
    "stopLoss": "110",
    "condicionesDeCambio": ["Deterioro de deuda", "Shock regulatorio"],
}

calls = {"n": 0}

def fake_call(prompt, max_tokens, use_search=True, system=None):
    calls["n"] += 1
    if calls["n"] == 1:
        assert use_search is True
        return R1, {"input_tokens": 500, "output_tokens": 300, "web_search_requests": 2}, [{"url":"https://example.com/a","title":"A"}], json.dumps(R1)
    if calls["n"] == 2:
        assert use_search is True
        return R2, {"input_tokens": 600, "output_tokens": 350, "web_search_requests": 3}, [{"url":"https://example.com/b","title":"B"}], json.dumps(R2)
    if calls["n"] == 3:
        assert use_search is False
        return R3, {"input_tokens": 700, "output_tokens": 400, "web_search_requests": 0}, [], json.dumps(R3)
    raise AssertionError("Sólo deberían existir 3 llamadas")


def main():
    tmp = Path("/tmp/agente_inversion_smoke")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()

    agente.CORRIDAS_DIR = tmp / "corridas"
    agente.HISTORIAL_PATH = tmp / "historial.json"

    with patch.object(agente, "call_claude", side_effect=fake_call):
        result = agente.analizar("SIMULADO_SMOKE_TEST")

    assert calls["n"] == 3
    assert result["salida_final"]["veredicto"] == "Comprar"
    assert result["uso"] == {"input_tokens": 1800, "output_tokens": 1050, "web_search_requests": 5}
    assert result["costo_estimado"]["web_search_usd"] == 0.05
    assert result["rondas"]["ronda1"]["raw_output"]
    assert len(result["salida_final"]["fuentes"]) == 2

    run_dir = agente.guardar_corrida(result)
    for required in ["entrada.md", "fecha.txt", "salida.json", "corrida.json"]:
        assert (run_dir / required).exists(), required
    manifest = json.loads((agente.CORRIDAS_DIR / "manifest.json").read_text(encoding="utf-8"))
    assert len(manifest) == 1
    assert manifest[0]["instrumento"] == "SIMULADO_SMOKE_TEST"

    shutil.rmtree(tmp)
    print("✓ SMOKE TEST OK — 3 rondas, raw outputs, fuentes, costos, estructura y manifest validados.")


if __name__ == "__main__":
    main()
