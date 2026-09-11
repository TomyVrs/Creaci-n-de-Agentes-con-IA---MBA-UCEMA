# Análisis económico

## Qué se mide

Cada corrida guarda métricas reales informadas por la API:

- tokens de entrada;
- tokens de salida;
- cantidad de búsquedas web ejecutadas;
- costo de tokens;
- costo de búsquedas;
- costo total estimado de la corrida.

La tabla final **no se completa a mano con números inventados**. Se genera a partir de los `corrida.json` reales con:

```bash
python resumen_economico.py
```

## Precios usados

Para `claude-sonnet-4-6`, el cálculo usa:

- USD 3 por 1 millón de tokens de entrada;
- USD 15 por 1 millón de tokens de salida;
- USD 10 por 1.000 búsquedas web (= USD 0,01 por búsqueda).

Estos valores deben volver a verificarse si cambia el modelo o antes de la entrega definitiva.

## Corridas reales

**Estado actual: pendiente.** La consigna exige al menos tres corridas reales y todavía no están incluidas en esta versión del repo.

| Corrida | Instrumento | Input tokens | Output tokens | Web searches | Costo total USD |
|---|---|---:|---:|---:|---:|
| 1 | pendiente | — | — | — | — |
| 2 | pendiente | — | — | — | — |
| 3 | pendiente | — | — | — | — |

## Proyección

Cuando existan al menos tres corridas, `resumen_economico.py` calcula el costo promedio real y proyecta automáticamente:

- 1 corrida por día: 365 corridas/año;
- 10 corridas por semana: 520 corridas/año.

Hasta entonces no se presenta una proyección como si fuera observada.

## Elección de modelo

La implementación actual usa `claude-sonnet-4-6` porque es el modelo con el que se construyó y depuró la arquitectura de tres rondas. La decisión se considera **provisional hasta preservar evidencia comparativa** contra un modelo más chico sobre la misma tarea. Si un modelo menor produce JSON válido, evidencia equivalente y una decisión comparable de manera consistente, el criterio de la materia indica preferir ese modelo menor.

Esto corrige una debilidad de la versión anterior: no se afirma como hecho una comparación Haiku/Sonnet si esa evidencia no está adjunta al repo.
