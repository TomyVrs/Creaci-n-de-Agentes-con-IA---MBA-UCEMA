# Agente de Análisis de Inversión

Trabajo final — Programación de y con Agentes de IA · MBA UCEMA · 2026 2T

## Qué construí

Construí un agente que recibe un instrumento financiero y ejecuta tres rondas encadenadas: investigación inicial con búsqueda web, búsqueda dirigida para cerrar gaps y una síntesis final sin nuevas búsquedas. La salida es un JSON estructurado con evidencia a favor/en contra, autocrítica, variable crítica, veredicto, confianza y líneas de corte.

El agente **no ejecuta operaciones**. Investiga y propone; la decisión y cualquier acción sobre dinero real quedan siempre del lado humano. El esquema de supervisión está documentado en [`GOBIERNO_Y_RIESGO.md`](./GOBIERNO_Y_RIESGO.md).

## Cómo se lo pedí

El contrato completo está en:

- [`prompts/system_prompt.md`](./prompts/system_prompt.md): rol, objetivo, contexto, tarea, restricciones, formato y ejemplo.
- [`prompts/user_prompt.md`](./prompts/user_prompt.md): las tres variantes del pedido puntual, una por ronda.

La implementación usa esos mismos prompts como fuente de ejecución. `agente.py` lee las variantes de `user_prompt.md`, reemplaza únicamente los datos variables de cada corrida y conserva en el artefacto final tanto la salida parseada como el texto crudo devuelto por el modelo.

## Qué funciona

- Tres rondas encadenadas.
- Búsqueda web real en Ronda 1 y Ronda 2.
- Ronda 3 sin búsqueda nueva: decide únicamente sobre la evidencia ya recuperada.
- JSON estricto y validación de parseo.
- Preservación del texto crudo de cada respuesta.
- Fuentes citadas de las rondas de investigación.
- Conteo real de tokens y cantidad de búsquedas web informada por la API.
- Cálculo de costo de tokens + búsquedas web.
- Historial local para calibrar confianza con resultados anteriores marcados por un humano.
- Smoke test sin consumo de API.
- Cada corrida real se guarda en una carpeta independiente con `entrada.md`, `fecha.txt`, `salida.json` y `corrida.json`; además se actualiza `corridas/manifest.json`.

### Cómo correrlo

Requiere Python 3.10+.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python test_smoke.py

# Definir ANTHROPIC_API_KEY en el entorno y luego:
python agente.py "NVDA"
```

Para generar las tres evidencias mínimas de entrega:

```bash
python agente.py "NVDA"
python agente.py "Bitcoin"
python agente.py "YPF"
```

## Qué falta o qué falló

### Pendiente obligatorio antes de entregar

Todavía faltan **tres corridas reales** guardadas en `corridas/`. No se incluyen corridas simuladas como sustituto porque la consigna pide evidencia real y reconstruible.

Una vez generadas las tres corridas:

1. verificar que cada carpeta tenga `entrada.md`, `fecha.txt`, `salida.json` y `corrida.json`;
2. correr `python resumen_economico.py`;
3. copiar la tabla resultante a [`ANALISIS_ECONOMICO.md`](./ANALISIS_ECONOMICO.md);
4. revisar manualmente las fuentes y la autocrítica de cada salida antes de considerar cerrada la entrega.

### Falla real que cambió la arquitectura

En desarrollo, una versión de una sola llamada se cortaba antes de terminar el JSON cuando intentaba buscar en la web y redactar simultáneamente una salida larga. En lugar de resolverlo sólo aumentando `max_tokens`, se separó el flujo en tres rondas para desacoplar investigación y síntesis. La historia completa está en [`DECISIONES.md`](./DECISIONES.md).

## Qué aprendí

El principal aprendizaje fue que un agente no mejora solamente agregando instrucciones o un modelo más grande. La arquitectura del flujo importa: separar búsqueda de decisión hizo el sistema más estable y auditable. También quedó claro que una afirmación en un README no reemplaza evidencia: las corridas reales, los outputs crudos y el uso medido de tokens son parte del sistema, no documentación opcional.

## Estructura

```text
README.md
DECISIONES.md
GOBIERNO_Y_RIESGO.md
ANALISIS_ECONOMICO.md
requirements.txt
agente.py
resumen_economico.py
test_smoke.py
prompts/
  system_prompt.md
  user_prompt.md
corridas/
  LEEME.md
  manifest.json              # aparece al ejecutar la primera corrida real
  corrida_YYYYMMDD_HHMMSS_x/
    entrada.md
    fecha.txt
    salida.json
    corrida.json
```

## Modelo

La versión de desarrollo usa `claude-sonnet-4-6`. Se mantiene ese modelo para que las corridas finales sean comparables con el proceso documentado. Los precios usados en el cálculo están documentados en [`ANALISIS_ECONOMICO.md`](./ANALISIS_ECONOMICO.md). La elección final del modelo debe justificarse con evidencia de calidad, no sólo con precio; por eso cualquier comparación con un modelo menor debe guardarse si se realiza.

## Disclaimer

Este proyecto es académico y de apoyo a decisiones. No constituye asesoramiento financiero y nunca ejecuta operaciones.
