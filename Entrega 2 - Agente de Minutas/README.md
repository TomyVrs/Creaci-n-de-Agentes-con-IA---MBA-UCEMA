# Agente para generación de minutas ejecutivas

## Qué construí

Construí un agente para generar minutas ejecutivas a partir de audios, transcripciones, notas de reunión o una combinación de esas fuentes.

El objetivo es delegar una tarea recurrente de trabajo: transformar información desordenada de una reunión en una salida estructurada que permita identificar rápidamente decisiones, acciones, responsables, plazos y temas críticos. Para documentar la entrega en un repositorio público utilicé un caso completamente sintético, sin información confidencial real de la empresa.

## Cómo se lo pedí

El contrato inicial se diseñó usando las seis piezas vistas en clase: **rol, contexto, tarea, restricciones, formato y ejemplos**.

### System prompt inicial (V1)

# System Prompt V1

## 1. Rol

Sos un asistente que me ayuda a armar minutas de reuniones a partir de audios, transcripciones o notas.

Tu función es ordenar la información de la reunión y dejar claro qué se habló, qué se decidió y qué quedó pendiente.

## 2. Contexto

La minuta se va a usar como registro de reuniones de trabajo.

La información puede venir de:
- audio de la reunión;
- transcripción;
- notas tomadas durante la reunión;
- o una combinación de esas fuentes.

La idea es que alguien que lea la minuta después pueda entender los principales temas tratados y los próximos pasos.

## 3. Tarea

Tenés que revisar toda la información disponible y armar una minuta que incluya:
- datos básicos de la reunión
- principales temas tratados
- decisiones tomadas
- acciones o próximos pasos
- responsables
- fechas o plazos, si se mencionaron
- temas que quedaron pendientes.

## 4. Restricciones

- No inventes información.
- Si no está claro quién es responsable de algo, poné `No definido`.
- Si no se definió una fecha o plazo, poné `No definido`.
- No presentes como decisión algo que solamente se propuso o discutió.
- Si hay información poco clara o contradictoria, indicá `Requiere validación`.
- No hace falta incluir saludos, charlas informales, repeticiones o comentarios que no aporten al contenido de la reunión.
- No agregues opiniones o recomendaciones propias.

## 5. Formato

Quiero que la salida mantenga siempre esta estructura:

### Datos de la reunión
Fecha:
Tema:
Participantes:
Objetivo:

### Resumen
Un resumen corto con los principales puntos.

### Temas tratados
| Tema | Resumen |
|---|---|

### Decisiones
| Decisión | Tema | Comentarios |
|---|---|---|

### Próximas acciones
| Acción | Responsable | Fecha | Estado |
|---|---|---|---|

### Temas pendientes
| Tema | Qué falta definir | Responsable |
|---|---|---|

## 6. Ejemplos

### Ejemplo 1
Si en la reunión dicen: "Tenemos que revisar el forecast antes de la próxima reunión."

La acción debería quedar así:

| Acción | Responsable | Fecha | Estado |
|---|---|---|---|
| Revisar el forecast | No definido | Antes de la próxima reunión | Pendiente |

### Ejemplo 2
Si dicen: "Podríamos evaluar trabajar con otro proveedor, pero primero tenemos que revisar costos."

Eso no debe figurar como una decisión tomada. Debe quedar como una propuesta o tema pendiente de evaluación.


### User prompt

# User Prompt

Necesito que armes la minuta de esta reunión usando las reglas del system prompt.

Fecha: [completar]
Tema de la reunión: [completar]
Participantes: [completar]

Material disponible:
- Audio: [sí / no]
- Transcripción: [sí / no]
- Notas: [sí / no]

Te adjunto el material disponible.

Usá toda la información para armar la minuta.

Si hay algo que no se entiende bien o se contradice entre las fuentes, marcá que requiere validación.

Usá el formato definido en el system prompt.


Después de cada corrida guardé la salida, identifiqué una falla concreta y modifiqué una sola pieza del contrato antes de volver a ejecutar el mismo caso.

Las versiones completas están guardadas en la carpeta `versiones/`.

## Qué funciona

- El agente transforma notas desordenadas de una reunión en una minuta estructurada.
- Diferencia decisiones tomadas de propuestas o temas todavía abiertos.
- Identifica acciones concretas y responsables.
- Cuando no hay una persona asignada, puede inferir el área responsable y lo indica explícitamente.
- Utiliza los plazos mencionados en la reunión y, si faltan, propone un plazo estimado en días.
- Marca información faltante que debe completarse antes de enviar la minuta.
- Identifica temas críticos mediante un semáforo y muestra riesgos, escenarios y decisiones requeridas.
- La versión final V4 reduce repeticiones y prioriza una lectura ejecutiva breve.
- Se ejecutó el mismo caso sintético en cuatro corridas, lo que permitió comparar directamente el efecto de cada cambio.

## Qué falta o qué falló

### Iteración 1 — de V1 a V2

**Qué falló:** la primera corrida dejó numerosos responsables y fechas como `No definido`, aunque por el tipo de tema podía inferirse al menos el área responsable y un plazo razonable. Además, esos campos podían llegar incompletos a una minuta destinada a enviarse por mail.

**Pieza modificada:** `Restricciones`.

**Cambio:** se permitió inferir el área responsable, estimar plazos cuando no existían y marcar los datos que debían completarse antes del envío.

**Resultado:** la segunda corrida asignó áreas responsables, diferenció las inferencias de los acuerdos explícitos y agregó plazos estimados.

### Iteración 2 — de V2 a V3

**Qué falló:** la segunda corrida registraba correctamente los temas y acciones, pero no indicaba cuáles eran críticos ni ayudaba a visualizar riesgos, escenarios o decisiones pendientes.

**Pieza modificada:** `Formato`.

**Cambio:** se agregó una sección de alertas con semáforo, escenarios y decisiones requeridas.

**Resultado:** la tercera corrida agregó una lectura ejecutiva de los asuntos críticos y permitió diferenciar temas simplemente informativos de temas que requerían intervención.

### Mejora adicional — de V3 a V4

**Qué falló:** la tercera corrida era demasiado extensa y repetía la misma información en varias secciones. Para una minuta, esto iba en contra del objetivo de lectura rápida.

**Pieza modificada:** `Formato`.

**Cambio:** se eliminó contenido redundante, se limitaron resumen, acciones y alertas, y se simplificó la estructura.

**Resultado:** la cuarta corrida quedó más breve, concreta y focalizada, manteniendo decisiones, acciones y alertas sin convertir la minuta en un informe largo.

### Nota de confidencialidad

La tarea real se aplica a reuniones que pueden contener información comercial sensible. Por ese motivo, **ninguna nota, audio, transcripción, nombre, empresa, cliente, cifra o decisión confidencial real fue incluida en este repositorio**. Las pruebas publicadas usan un caso sintético diseñado para conservar el tipo de dificultad de una reunión real sin exponer información de la empresa.

## Qué aprendí

Aprendí que un prompt útil para una tarea recurrente funciona mejor cuando se lo trata como un contrato y no como un pedido aislado. Las seis piezas ayudan a diagnosticar exactamente qué parte debe corregirse cuando la salida falla.

También comprobé que agregar más información o más secciones no siempre mejora el resultado: la V3 tenía más contenido y más análisis, pero era menos útil como minuta. La V4 mejoró cuando el formato obligó al agente a priorizar y sintetizar.

Por último, entendí la importancia de modificar una sola pieza por vez y volver a correr el mismo caso, porque así se puede observar qué cambio produjo realmente la mejora.
