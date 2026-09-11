<!--
Fuente del framework de niveles de autonomía (L0-L4): deck/clase1_agente.html
del repo de la materia (rail "Autonomía y supervisión", sección "Niveles de
delegación"), con el complemento de deck/clase3_agente.html sobre el
circuito propuesta → revisión → aprobación. Verificado por el alumno.
-->

# Gobierno y riesgo

## El framework de la materia

> «La pregunta profesional no es "¿puede hacerlo solo?" sino "¿qué pasa si
> lo hace mal, y quién firma?" La responsabilidad no se delega.»
> — deck/clase1_agente.html

Niveles de delegación (deck/clase1_agente.html):

| Nivel | Nombre | Qué pasa |
|---|---|---|
| L0 | Consultar | El humano pregunta, la IA responde. Nada se ejecuta. |
| L1 | Proponer | La IA redacta o planifica; el humano aprueba cada paso. |
| L2 | Ejecutar con revisión | El agente trabaja solo; el humano revisa hitos y el final. *(nivel por defecto de la materia)* |
| L3 | Ejecutar y avisar | El agente entrega; el humano audita por muestreo. |
| L4 | Autónomo | Sin humano en el loop. Reservado para tareas donde el error es barato y reversible. |

## Qué sistemas toca el agente

- **Lectura**: internet, vía la herramienta de búsqueda web de la API de Anthropic (rondas 1 y 2). Solo lectura, no hay escritura a ningún sistema externo.
- **Escritura**: únicamente al sistema de archivos local del repo (`corridas/*.json`, `historial.json`). No toca cuentas bancarias, brókers, ni ningún sistema con dinero real o credenciales de terceros.

## Nivel de autonomía por etapa

| Etapa | Nivel | Qué hace el agente solo | Qué hace/revisa el humano |
|---|---|---|---|
| Rondas 1 y 2 (investigar) | **L2 — Ejecutar con revisión** | Busca, filtra y sintetiza información pública en varios pasos encadenados | Audita las fuentes citadas y el resultado antes de confiar |
| Ronda 3 (decidir) | **L1 — Proponer** | Redacta el veredicto, la autocrítica y las líneas de corte | Tiene que aprobar explícitamente antes de cualquier acción real |
| Ejecución de una operación | *(no existe en este sistema)* | El agente nunca ejecuta | El humano ejecuta fuera del sistema |
| Calibración por historial | **L2 — Ejecutar con revisión** | Ajusta la confianza usando el historial marcado | El humano marca `resultado_real` a mano |

El sistema completo nunca supera **L1** en el punto que importa: actuar con dinero real.

## Circuito de aprobación

1. **Propuesta**: la Ronda 3 entrega el veredicto completo.
2. **Revisión**: el humano revisa fuentes, autocrítica, variable frágil y líneas de corte.
3. **Aprobación**: cualquier acción real ocurre fuera del sistema y sólo por decisión humana.

## Qué puede salir mal

1. **Alucinación de un nivel técnico**: se mitiga exigiendo `no disponible` cuando el dato no aparece en la investigación.
2. **Búsqueda desactualizada o sesgada**: se mitiga buscando desacuerdo activamente y revisando fuentes.
3. **Sobreconfianza pese a evidencia mixta**: se mitiga con autocrítica e historial, pero requiere revisión humana.
4. **Prompt injection desde una fuente web**: una página puede contener instrucciones dirigidas al modelo. Se mitiga tratando todo contenido web como evidencia no confiable y ordenando ignorar instrucciones encontradas en fuentes externas.
5. **Fallo técnico a mitad de proceso**: la arquitectura de tres rondas reduce el riesgo de truncamiento, pero la API o la red pueden fallar.

## Qué revisa el humano antes de confiar

- precio de referencia contra una fuente propia;
- fuentes citadas;
- variable más frágil y autocrítica;
- líneas de corte y consistencia con su propio criterio de riesgo.

## Quién firma

El humano que corre el script es quien firma. No hay firma automática ni ejecución downstream. La responsabilidad no se delega.
