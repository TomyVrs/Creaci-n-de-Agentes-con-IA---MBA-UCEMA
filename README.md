# Calculadora de Costos y Precio Objetivo para Aires Acondicionados

## Que construi

Construi una app web simple en HTML para costear varios SKUs de aires acondicionados residenciales.
La herramienta permite trabajar por mes, cargar tarifas generales, datos de cada producto, tipo de cambio, precio de venta con IVA, plazo de cobro, TNA y unidades.
Calcula automaticamente el precio sin IVA, la desgravacion, el costo total, margen bruto, costo financiero y margen neto.
Esta pensada para un Gerente de Negocio/Producto que necesita automatizar estructuras de costo y analizar rentabilidad por SKU y por mes.

## Como se lo pedi

Prompts principales usados durante el proceso:

1. "Soy principiante total. Tengo Windows 11 y quiero, mediante codex que ya tengo instalado, programar con IA sin usar la terminal. Guiame paso a paso, uno por vez, y espera mi confirmacion antes de seguir."

2. "Me gustaria que existiera una app, html o el formato que mas convenga que me permita automatizar esto. Dame 10 ideas de cosas que podria construir con IA para eso, de la mas obvia a la mas rara."

3. "1 y 7 me parecen bien. No tenemos que armar algo grande que se nos vaya de escala. Ademas, necesito que documentemos todo el proceso, ya que debo entregarlo en la materia Creacion de Agentes de IA del MBA de UCEMA."

4. "La idea base esta bien, pero quisiera que sea mas robusto o bien, que el calculo del costo sea en base a diferentes tarifas para cada concepto de costeo. Es decir, el input deberian ser ciertas tarifas, y el costeo deberia ser automatico con difrentes formulas segun el costo."

5. "Los rubros del costeo van a ser los siguientes: Precio FOB; Logistica Internacional; Logistica Local IDA; Costo Produccion; Logistica Local VUELTA; Costo Almacenamiento; Costo Distribucion; Impuestos; Costo Total; Precio de Venta sin IVA; Precio de Venta con IVA; Margen; Margen %; Unidades."

6. "Varios"

7. "Logistica Internacional = Flete internacional/Stuffing contenedor; Logistica Local IDA = Flete local IDA/Stuffing camion IDA; Costo Produccion = Costo horario x Tiempo estandar + Scrap % x Precio venta sin IVA; Logistica Local VUELTA = Flete local VUELTA/Stuffing camion VUELTA; Costo Almacenamiento = IN deposito + OUT deposito; Costo Distribucion = Tarifa distribucion x m3 producto; Impuestos = Precio venta sin IVA x (IIBB % + Debito/Credito %); Costo Total = suma de todos los costos; Precio venta con IVA = Precio venta sin IVA x (1 + IVA %); Margen = Precio venta sin IVA - Costo Total; Margen % = Margen / Precio venta sin IVA."

8. "Hay costos en pesos y otros en dolares. Asi que debemos tener como input el tipo de cambio tambien. El costeo deberiamos poder verlo en pesos o en dolares (lo mismo con el precio de venta)."

9. "Me gustaria llevar el margen bruto a neto (solo afectado por financiacion, asociada al plazo de venta). Asi que deberiamos tener una TNA que segun el plazo (en dias) que defina para el precio, afecte el margen."

10. "Tomemos 360 dias para el calculo en lugar de 365."

11. "Va bien, pero quiero algunos ajustes y revisiones: Resumen consolidado: Quisiera ver los % de los margenes y el costo financiero. El costo total no me interesa tenerlo ahi. Ajustes visuales: Hace la app mas moderna, mejora el estilo, organiza mejor cada modulo. Utiliza una paleta de colores con tonos de azules, grises y blancos, mas similar a la marca BGH. Proximo paso, ademas, quisiera poder mensualizar esto. Es decir, para cada mes poder setear las diferentes variables, precios, cantidades, tasa y tipo de cambio. Todas la variables."

12. "Quisiera ahora que agreguemos un dashboard, donde se pueda ver el consolidado en venta, unidades, margen bruto ($ y %) y margen neto ($ y %). Esto deberia ser consolidado a la fecha que yo quiera. Agreguemos cards y graficos con la apertura de los rubro de la estructura, para poder entender el peso relativo de cada uno dentro del costeo del producto. Ademas, quisiera poder seleccionar uno o mas modelos, total, es decir, diferentes variantes y filtros en el dashboard. El dashboard quiero poder definir yo los meses que quiero totalizar."

13. "Debemos agregar una complejidad al costeo. La desgravacion es un beneficio impositivo que aplica al precio. La desgravacion suma al precio. El margen final se debe calcular considerando el precio sin IVA + desgravacion. Sumemos la desgravacion como un input general. El estandar es 21%. Por otro lado, el precio que quiero cargar es el precio con IVA, que la app luego calcule todo el resto. La desgravacion se aplica al precio sin IVA."

14. "Ajustes y cambios: mejorar el dashboard, agregar conclusiones, traer tipo de cambio futuro desde Rofex, hacer mes y anio configurables, hacer modulos contraibles, cargar productos desde una planilla Excel/template y buscar la ultima tasa BADLAR del BCRA."

15. "El tipo de cambio debe salir de la tabla Cierre Monedas de MATBA Rofex, salvo que sea un mes pasado. Si es un mes cerrado, que traiga el tipo de cambio Divisa Vendedor del BNA del ultimo dia de cada mes."

16. "La tasa BADLAR tambien es un dato publico, necesito que apliques la misma logica que con el tipo de cambio para los meses cerrados. Para el mes vigente y futuro, necesito que tomes la del dia publicada."

17. "Quiero tener un selector general donde elija si quiero ver en USD o PES los datos, resumen, etc. Si una variable esta cargada en PES, debe dolarizarla al TC del mes asociado o viceversa. Si es un input, yo puedo cargar en USD o PES, y debe dolarizar o pesificar de acuerdo al TC."

18. "No me actualiza el TC correctamente: no encontro DLR082026 en Cierre monedas, pero en la web de Rofex se ve en la columna Ajuste que DLR082026 es 1501,5."

19. "La tasa BADLAR tampoco la actualiza: no encontro la variable BADLAR Bancos Privados en BCRA."

20. "El TC no actualiza bien: para meses cerrados no actualiza y para meses futuros toma siempre el mismo valor de Agosto."

21. "Meses cerrados: toma mal la unidad; Julio devuelve 14470000,00 cuando el correcto es 1.485. Mes vigente: debe tomar Rofex, no el ultimo mes cerrado."

22. "Quiero que la app me sugiera el precio target para meses futuros para mantener el margen neto del mes vigente. Meses cerrados y actual: precio manual o template. Tambien quiero saber como venimos contra inflacion, devaluacion y evolucion de costos, tomando el SKU mas representativo o uno elegido."

23. "La actualizacion de TC quiero que sea general: futuros Rofex juntos y meses cerrados juntos. Para precios, quiero target por margen vigente o margen objetivo, y respetar un gap fijo entre SKUs mediante price index contra un modelo referencia."

24. "La sugerencia de precios futuros debe ser completa para toda la serie 12 meses vista. El price index, criterio de margen y scrap deben ser configurables de forma general, aunque pueda modificarlo dentro de un mes puntual."

25. "La actualizacion de variables macro y futuras debe distinguir mes seleccionado de mes vigente real. El mes vigente siempre es el mes calendario real, no el mes seleccionado en la app. Revisar titulos."

26. "En las conclusiones quiero que tambien haya conclusiones respecto a variacion de costos, inflacion, devaluacion y precios. Separar y mejorar la visual del dashboard: resumen, comparativas, analisis y conclusiones."

## Que funciona

La app funciona abriendo el archivo `index.html` en un navegador.
Permite seleccionar un mes de trabajo y cargar variables distintas para cada mes.
Cada mes guarda sus propios parametros generales, tarifas, precios, cantidades, plazos y SKUs en el navegador.

La tabla permite cargar varios SKUs con FOB, m3, tiempo estandar, precio de venta con IVA, moneda del precio, plazo de venta y unidades.
Cada cambio recalcula automaticamente:

- Precio FOB convertido a pesos
- Logistica internacional
- Logistica local IDA
- Costo de produccion
- Logistica local VUELTA
- Costo de almacenamiento
- Costo de distribucion
- Impuestos
- Costo total
- Precio de venta sin IVA
- Desgravacion sobre precio sin IVA
- Precio de venta con IVA cargado
- Margen bruto y margen bruto %
- Costo financiero
- Margen neto y margen neto %
- Resultado consolidado por unidades

La desgravacion se carga como porcentaje general del mes. El valor inicial estandar es 21%.
El margen se calcula usando esta base:

`Base de margen = Precio de venta sin IVA + Desgravacion`

`Margen bruto = Base de margen - Costo total`

El resumen consolidado muestra unidades, venta sin IVA, margen bruto, margen bruto %, costo financiero, margen neto y margen neto %.
El dashboard permite elegir un rango de meses, filtrar uno o mas modelos, y ver:

- Venta sin IVA consolidada
- Unidades consolidadas
- Margen bruto en pesos/dolares y en %
- Margen neto en pesos/dolares y en %
- Costo financiero
- Apertura de rubros de costo con barras de peso relativo
- Conclusiones automaticas sobre rubros relevantes, margen y costo financiero

Los modulos de la app se pueden contraer y expandir.
La app incluye dos templates de carga de productos:

- `template_productos.csv`
- `template_productos.xlsx`

El CSV funciona de forma local. El XLSX funciona si el navegador puede cargar la libreria de lectura de Excel desde internet.
Tambien se agrego un boton para intentar actualizar BADLAR desde la API publica del BCRA.
La app tiene un selector global de vista en PES o USD. Los inputs conservan su moneda original de carga, pero los calculos se realizan internamente en pesos y los resultados se muestran segun la vista seleccionada.
En el dashboard, si se elige USD y el periodo incluye varios meses, cada mes se dolariza con su propio tipo de cambio antes de consolidar.
El boton de actualizacion de tipo de cambio aplica esta regla:

- Mes vigente real o futuro: busca el contrato `DLRMMYYYY` en la API publica de CEM / MATBA Rofex y toma `settlement`, que corresponde a la columna Ajuste de Cierre Monedas.
- Mes cerrado: busca el ultimo dato disponible del mes en BNA y toma Divisa Vendedor.

Se corrigio el caso `DLR082026`: la primera version intentaba leer la tabla desde el HTML de `matbarofex.com.ar`, pero esa tabla se renderiza desde otra app. Ahora consulta el endpoint `https://apicem.matbarofex.com.ar/api/v2/closing-prices` ordenado por fecha descendente y toma el ultimo cierre disponible.
Como el navegador puede bloquear algunas lecturas desde un archivo local por CORS, la app intenta primero la fuente directa y despues respaldos publicos de lectura.
Se corrigio tambien el selector de mes usado para Rofex: el boton de TC ahora toma siempre el mes visible en pantalla para construir `DLRMMYYYY`. Se valido que `DLR092026` devuelve 1527,50 y `DLR102026` devuelve 1556,00.
Para meses cerrados, BNA se consulta con `idMoneda=55` (Dolar U.S.A). Si BNA devuelve mas de una cotizacion cercana, la app toma la venta exacta del dia buscado o, si no existe, la ultima anterior dentro del mismo mes.
Se corrigio el parseo de BNA: el valor puede venir como `1485.0000`, donde el punto es decimal, no separador de miles. La app usa un parser especifico para BNA para evitar inflar el tipo de cambio.
Tambien se ajusto la regla de mes cerrado: solo usa BNA si el periodo seleccionado es anterior al mes calendario actual. El mes vigente usa Rofex mientras no este cerrado.

El boton de actualizacion de BADLAR aplica esta regla:

- Mes vigente real o futuro: toma la ultima BADLAR publicada por BCRA.
- Mes cerrado: busca el ultimo dato BADLAR disponible dentro de ese mes en la API de BCRA.

Se corrigio la busqueda de BADLAR: BCRA publica la variable como `Tasa de interes BADLAR de bancos privados` con unidad `En porcentaje nominal anual`, no necesariamente con simbolo `%`. La app prioriza `idVariable 139` y, si cambia, busca por descripcion y TNA. Tambien se corrigio el parseo del valor porque BCRA puede devolver coma decimal.

La formula del costo financiero usa anio comercial de 360 dias:

`Costo financiero = Precio de venta sin IVA x TNA x Plazo en dias / 360`

Para precios futuros, la app agrega una columna `Precio target` y botones para sugerir el mes seleccionado o toda la serie futura.
La logica es:

- Mes cerrado y mes vigente real: precio manual o importado desde template.
- Mes futuro: calcula el precio con IVA necesario para mantener el margen neto % del mes vigente real o cumplir un objetivo de margen definido.
- La sugerencia considera costos del mes futuro, tipo de cambio, TNA, plazo, impuestos, scrap y desgravacion.

El dashboard tambien compara el periodo seleccionado contra variables macro:

- Inflacion oficial acumulada: IPC Nacional INDEC desde la API oficial de Series de Tiempo.
- Devaluacion acumulada: variacion del tipo de cambio cargado entre primer y ultimo mes con datos.
- Evolucion de precio del SKU base: precio sin IVA del primer mes vs ultimo mes del periodo.
- Evolucion de costo del SKU base: costo total unitario del primer mes vs ultimo mes del periodo.

El SKU base puede elegirse manualmente. Si queda en automatico, la app usa el SKU de mayor volumen dentro del periodo y filtros seleccionados.

Se reorganizo el dashboard en bloques:

- Resumen comercial.
- Comparativas del periodo.
- Analisis de costos.
- Conclusiones.

Las conclusiones ahora incluyen lecturas sobre margen, costo financiero, principal rubro de costo, inflacion oficial, devaluacion, evolucion de precios y evolucion de costos del SKU base.

Se agregaron botones de actualizacion macro:

- `Actualizar curva`: actualiza toda la curva Rofex del mes vigente real y meses futuros del anio de trabajo.
- `Actualizar cerrados`: actualiza meses cerrados del anio de trabajo con TC BNA y BADLAR BCRA. La inflacion oficial se refresca en el dashboard desde INDEC.

Se corrigio la interpretacion de mes vigente: la app compara cada periodo contra la fecha real del sistema. El selector de mes solo indica que mes se esta editando. Por ejemplo, con fecha real agosto 2026, julio 2026 es cerrado, agosto 2026 es vigente real y diciembre 2026 es futuro. Para Rofex, la app solo acepta el contrato exacto `DLRMMYYYY`; si no lo encuentra, no escribe otro mes por error.

Para precios target se agrego parametrizacion:

- Modo `Mantener margen neto % mes vigente real`.
- Modo `Margen neto objetivo %`.
- Modo `Margen neto objetivo $ unitario`.
- Selector de SKU referencia.
- Campo `Price_Index` por SKU, tambien incluido en los templates CSV/XLSX.

El calculo parte del SKU referencia y aplica el price index al resto para conservar el gap relativo de precios.

Se agrego una capa de configuracion general de pricing:

- `Guardar configuracion general`: guarda scrap, criterio de margen, SKU referencia y price index por SKU.
- `Aplicar general a 12 meses`: copia esa configuracion a todos los meses del anio de trabajo.
- `Sugerir futuros 12 meses`: calcula y aplica precios target en todos los meses futuros de la serie.

Cada mes queda editable luego de aplicar la configuracion general, funcionando como override mensual.

## Que falta o que fallo

La app ya guarda la informacion mensual en el navegador y permite importar productos desde template.
Si se abre en otro navegador o en otra computadora, no se transfieren automaticamente los datos cargados.
Todavia no tiene un P&L completo de categoria ni una vista grafica de evolucion mes a mes.
La actualizacion automatica de Rofex, BNA y BCRA depende de que el navegador permita leer esas fuentes desde un archivo HTML local. Si alguna fuente bloquea la consulta por CORS o cambia su estructura, los campos quedan editables manualmente.

Durante el proceso aparecio un problema de visualizacion de caracteres en el README clonado: algunas palabras se veian mal por codificacion.
Para evitar problemas de codificacion, el README fue reescrito usando texto simple y sin caracteres especiales.

Posibles mejoras futuras:

- Agregar una vista anual con comparacion mes a mes.
- Incorporar escenarios de tipo de cambio, precio, TNA y volumen.
- Separar tarifas por familia, canal, proveedor u origen.
- Exportar resultados a Excel.

## Que aprendi

Aprendi que trabajar con agentes de IA no es solamente pedir "haceme una app", sino ir definiendo reglas de negocio paso a paso.
Tambien entendi que conviene empezar con un alcance chico, pero suficientemente realista para que represente el problema.
El agente ayudo a transformar una necesidad de negocio en formulas, inputs, outputs y una primera herramienta usable.
La parte mas importante fue explicitar supuestos: moneda, tipo de cambio, tarifas, margen bruto, financiacion, plazo de venta y mensualizacion.
