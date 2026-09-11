# DECISIONES.md — La historia del proceso

Este agente no nació de una vez. Empezó como un prototipo interactivo (un
panel de inversión construido como artifact de React dentro de Claude.ai)
que fue creciendo en capas a lo largo de muchas iteraciones, y terminó
siendo el motor de decisión que este trabajo final reempaqueta como un
agente de script, con repo y corridas reales. Documento acá las decisiones
importantes, en orden, incluyendo las que fueron errores.

## 1. Primera versión: demasiado simple

El primer diseño era un solo llamado a la API que buscaba información y
devolvía un resumen con "a favor / en contra" por clase de activo (acciones,
bonos, cripto, forex). Servía como informador, pero no decidía nada — era
más cerca de un buscador con formato que de un agente.

**Decisión:** agregar un módulo separado donde el sistema investigara,
pesara la evidencia, y llegara a un veredicto propio (Comprar / Mantener /
Evitar / Reducir), en vez de solo mostrar información para que la persona
decida sola.

## 2. El agente "sonaba" convincente pero no razonaba de verdad

Con el veredicto agregado, quedaba un problema: el modelo podía sonar seguro
sin estar realmente calibrado. Se agregó un paso de **autocrítica** —
después de llegar al veredicto, el agente tiene que buscar el argumento más
fuerte EN CONTRA de su propia conclusión, y bajar su nivel de confianza si
ese argumento es sólido. Esto llevó a separar explícitamente, en cada punto
de evidencia, qué es un **Dato** (verificado buscando) de qué es una
**Interpretación** (lectura propia) — antes todo sonaba con el mismo peso
aunque la certeza real fuera muy distinta.

## 3. La falla real: el agente se cortaba a mitad de la respuesta

Al probar el sistema con un ticker real (YPF, que cotiza en la Bolsa de
Buenos Aires), empezó a fallar de forma reproducible con el error:

```
La respuesta se cortó por límite de longitud antes de terminar el JSON
```

Investigando la causa: la llamada que arma el veredicto final hacía
búsquedas web Y escribía el JSON grande (evidencia, autocrítica, líneas de
corte, comparación con alternativas) **en la misma llamada** — y los
resultados de búsqueda consumían presupuesto de tokens antes de que el
modelo llegara a escribir la respuesta completa.

**Decisión (la más importante del proyecto):** separar el proceso en 3
rondas encadenadas:
1. Investigación inicial (con búsqueda) → evidencia + preguntas sin resolver.
2. Búsqueda dirigida a esas preguntas específicas (con búsqueda) → niveles
   técnicos, comparable, tasa libre de riesgo.
3. Síntesis y decisión (**sin búsqueda**) → todo el presupuesto de tokens
   de esta llamada va directo a escribir el JSON final, sin competir con
   resultados de búsqueda.

Esto resolvió el problema de raíz, no con un parche (subir el límite de
tokens no alcanzaba por sí solo) sino cambiando la arquitectura de cuándo
busca y cuándo escribe. Quedó documentado también un manejo de errores por
ronda: si falla la ronda 2 o 3, el sistema no repite las rondas anteriores
desde cero (eso costaba tiempo y llamadas a la API innecesariamente).

## 4. Lo que se sacó por confundir más de lo que ayudaba

- Un sistema de "pesos" con sliders para que la persona ponderara criterios
  (valuación, momentum, macro, riesgo) — probamos que nadie entendía qué
  cambiaban ni por qué el resultado no se sentía objetivo si los números
  salían de los propios sliders del usuario. Se sacó por completo.
- Dos módulos que hacían casi lo mismo (una búsqueda rápida de niveles
  técnicos, separada de un análisis completo que terminó incluyendo esos
  mismos niveles) se dejaron coexistir pero con una diferenciación clara de
  cuándo usar cada uno, para no duplicar sin necesidad.

## 5. Achicar el alcance para esta entrega

La versión completa del prototipo (interactivo, con historial persistente,
gráficos, cartera real, comparador de escenarios) tiene 11 módulos — mucho
más de lo que esta consigna pide y, sobre todo, en un formato (artifact de
React corriendo dentro de Claude.ai) que un agente evaluador externo no
puede leer ni reproducir desde un repo.

**Decisión final:** para este trabajo, recortar al motor de decisión (las 3
rondas descriptas arriba), reempaquetado como script de Python con SDK de
Anthropic, con historial de aciertos persistido en un archivo JSON simple
en vez de en el storage del navegador. Es la pieza más agéntica y mejor
probada del sistema completo, y la única que tiene sentido evaluar con la
vara de este trabajo: contrato + herramienta real + supervisión + formato
reproducible.

## 6. Qué quedó afuera, a propósito

- Conectores adicionales (planilla, calendario): no se sumaron por el plazo
  de entrega — la búsqueda web ya es una herramienta real y funcional, y
  agregar una segunda sin tiempo de probarla sumaba riesgo sin sumar
  robustez real al sistema.
- Ejecución automática de operaciones: el agente nunca compra ni vende por
  su cuenta. Esto no es una limitación técnica — es una decisión de diseño
  documentada en GOBIERNO_Y_RIESGO.md.

## 7. Endurecimiento final para que la evidencia sea corregible

Al revisar el trabajo contra la consigna apareció una diferencia importante
entre "el código puede correr" y "un tercero puede reconstruir una corrida".
La primera versión guardaba un único JSON parseado y el README afirmaba que
existían corridas reales aun cuando todavía no estaban adjuntas. Eso era una
debilidad de evidencia, no de la idea del agente.

**Cambios:**

- cada corrida real ahora genera una carpeta con `entrada.md`, `fecha.txt`,
  `salida.json` y `corrida.json`;
- `corrida.json` conserva también el texto crudo de cada respuesta del modelo,
  además del JSON parseado;
- se guarda la cantidad de búsquedas web reportada por la API y se incorpora
  su costo al cálculo económico;
- se agregó un `manifest.json` para inventariar las corridas;
- se agregó protección explícita contra instrucciones maliciosas encontradas
  dentro de páginas web;
- el README dejó de afirmar que existen corridas reales mientras estén
  pendientes;
- la comparación contra modelos menores quedó marcada como pendiente de
  evidencia en vez de presentarse como un resultado demostrado.

Este cambio busca que la documentación sea más honesta y que el evaluador no
tenga que inferir qué pasó. Las tres corridas reales siguen siendo un paso
obligatorio que no puede reemplazarse por datos simulados.
