"""Resume costos reales de las corridas guardadas. No inventa datos faltantes."""

import json
from pathlib import Path

ROOT = Path(__file__).parent
CORRIDAS = ROOT / "corridas"

files = sorted(CORRIDAS.glob("corrida_*/corrida.json"))
if not files:
    raise SystemExit("No hay corridas reales todavía.")

rows = []
for path in files:
    data = json.loads(path.read_text(encoding="utf-8"))
    uso = data.get("uso", {})
    costo = data.get("costo_estimado", {})
    rows.append({
        "instrumento": data.get("instrumento"),
        "input": uso.get("input_tokens", 0),
        "output": uso.get("output_tokens", 0),
        "searches": uso.get("web_search_requests", 0),
        "cost": costo.get("total_usd", 0),
    })

print("| Corrida | Instrumento | Input tokens | Output tokens | Web searches | Costo total USD |")
print("|---:|---|---:|---:|---:|---:|")
for i, row in enumerate(rows, 1):
    print(f"| {i} | {row['instrumento']} | {row['input']} | {row['output']} | {row['searches']} | {row['cost']:.6f} |")

avg = sum(r["cost"] for r in rows) / len(rows)
print(f"\nCosto promedio real: USD {avg:.6f} por corrida")
print(f"1 corrida/día: USD {avg*365:.2f}/año")
print(f"10 corridas/semana: USD {avg*520:.2f}/año")
