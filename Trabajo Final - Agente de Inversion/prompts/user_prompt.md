# User Prompt — 3 variantes (una por ronda)

A diferencia de `system_prompt.md` (la identidad estable del agente), este
archivo es el **pedido puntual y los datos variables de cada corrida**:
qué instrumento, qué fecha, y qué encontraron las rondas anteriores. Cada
variante se envía como el mensaje de usuario de una llamada distinta a la
API, encadenadas por el script `agente.py`. `{instrumento}`, `{fecha}` y
los demás `{...}` los completa el script en tiempo de ejecución con los
datos reales de esa corrida.

---

## Variante 1 — Ronda 1 (investigación inicial)

```
Actuás como un analista investigando "{instrumento}" HOY ({fecha}). Hacé
varias búsquedas: datos actuales, catalizadores recientes, medios
financieros especializados, y opiniones de analistas divergentes entre sí
(buscá activamente desacuerdo, no solo consenso). Si "{instrumento}" cotiza
en una bolsa específica, aclaralo en tu búsqueda para no confundir tickers
parecidos de otros mercados.

Respondé SOLO JSON, sin texto antes ni después:
{"precioReferencia":"precio o nivel actual exacto, o 'no disponible'",
"evidenciaAFavor":["máximo 4 items, frases cortas"],
"evidenciaEnContra":["máximo 4 items, frases cortas"],
"gapsDeInformacion":["2 a 3 preguntas concretas y específicas que todavía
no pudiste responder bien"]}
```

---

## Variante 2 — Ronda 2 (búsqueda dirigida)

```
Estás investigando "{instrumento}" ({fecha}). Ya encontraste esto:
Evidencia a favor: {evidenciaAFavor_ronda1}
Evidencia en contra: {evidenciaEnContra_ronda1}
Preguntas sin resolver: {gapsDeInformacion_ronda1}

Hacé búsquedas NUEVAS Y ESPECÍFICAS para responder esas preguntas. Además,
buscá niveles técnicos publicados si existen: soporte, resistencia, zona de
entrada, objetivo de ganancia y stop-loss. Buscá también un activo
comparable/competidor directo, y la tasa libre de riesgo actual.

Respondé SOLO JSON, breve y compacto, sin texto antes ni después:
{"gapsResueltos":[{"pregunta":"breve","respuesta":"breve, máximo 20
palabras"}],
"evidenciaAdicionalAFavor":["máximo 2 items"],
"evidenciaAdicionalEnContra":["máximo 2 items"],
"nivelesTecnicos":{"zonaEntrada":"o 'no encontrado'","tomarGanancia":"o 'no
encontrado'","stopLoss":"o 'no encontrado'","soporte":"o 'no
encontrado'","resistencia":"o 'no encontrado'"},
"comparable":"nombre de un competidor/activo comparable",
"tasaLibreRiesgo":"valor actual aproximado"}
```

---

## Variante 3 — Ronda 3 (síntesis y decisión, sin búsqueda)

```
Tenés toda la investigación ya hecha sobre "{instrumento}" ({fecha}), no
necesitás buscar nada más — solo razonar con lo que sigue:

Precio de referencia: {precioReferencia}
Evidencia a favor: {evidenciaAFavor_combinada}
Evidencia en contra: {evidenciaEnContra_combinada}
Preguntas investigadas y sus respuestas: {gapsResueltos}
Niveles técnicos encontrados: {nivelesTecnicos}
Activo comparable: {comparable} · Tasa libre de riesgo: {tasaLibreRiesgo}
Historial de aciertos del sistema: {hitRateTexto}

Tareas (sé conciso, frases cortas):
1. Para CADA punto de evidencia, marcalo como "Dato" (verificado) o
   "Interpretación" (lectura propia). No inventes evidencia nueva.
2. Resolvé la contradicción entre la evidencia — por qué un lado pesa más
   ahora, en máximo 3 frases.
3. Identificá LA VARIABLE MÁS FRÁGIL: una sola frase concreta.
4. Compará contra la tasa libre de riesgo y contra el comparable.
5. Veredicto (Comprar/Mantener/Evitar/Reducir) y confianza (Alta/Media/Baja)
   — calibrada por el historial de aciertos de arriba.
6. Autocrítica: el argumento más fuerte en contra de tu propio veredicto.
7. Líneas de corte: usá los niveles técnicos de arriba; si no hay, "no
   disponible" — nunca inventar un número.

Respondé SOLO JSON, sin texto antes ni después:
{"instrumento":"{instrumento}","precioReferencia":"...",
"evidenciaAFavor":[{"texto":"...","tipo":"Dato o Interpretación"}],
"evidenciaEnContra":[{"texto":"...","tipo":"Dato o Interpretación"}],
"resolucion":"máximo 3 frases","varianteCritica":"una sola frase",
"comparacionAlternativas":{"cash":"1 frase","alternativa":"...",
"comparacion":"1 frase"},
"veredicto":"Comprar/Mantener/Evitar/Reducir","confianza":"Alta/Media/Baja",
"calibracion":"1 frase","autocritica":"máximo 3 frases",
"posicionSugerida":"breve","horizonteRecomendado":"breve",
"zonaEntrada":"...","tomarGanancia":"...","stopLoss":"...",
"condicionesDeCambio":["breve","breve"]}
```
