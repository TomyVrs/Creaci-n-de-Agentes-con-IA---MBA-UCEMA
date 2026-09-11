# Corridas reales

Esta carpeta debe contener al menos tres ejecuciones reales del agente. Cada ejecución genera una subcarpeta con `entrada.md`, `fecha.txt`, `salida.json` y `corrida.json`.

`corrida.json` conserva la trazabilidad completa de las tres rondas: prompts renderizados, salida cruda y parseada, fuentes, tokens, búsquedas web y costo estimado.

El archivo `manifest.json` se crea automáticamente con la primera corrida y se actualiza con las siguientes. Después de completar tres corridas, usar `resumen_economico.py` para generar la tabla económica basada en datos reales.
