# Registro de iteraciones

## Iteración 1 — V1 → V2

**Falla observada**

La primera salida dejó numerosos responsables y fechas como `No definido`, aunque por el contenido era posible inferir al menos un área responsable y un plazo razonable. Además, esos campos quedarían incompletos en una minuta destinada a enviarse por mail.

**Pieza modificada:** 4. Restricciones.

**Cambio realizado**
- Inferir el área responsable cuando no hubiera una persona explícitamente asignada.
- Usar primero los plazos mencionados y, si faltaban, estimar un plazo razonable en días.
- Identificar los datos que debían completarse antes del envío.
- Señalar explícitamente las inferencias para no confundirlas con acuerdos de la reunión.

**Qué cambió en la salida**
- Los responsables pasaron de `No definido` a áreas como `Ventas`, `Negocio` o `Finanzas`, identificadas como inferidas cuando correspondía.
- Las acciones sin fecha recibieron plazos estimados.
- Los faltantes relevantes pasaron a marcarse como `A completar antes de enviar`.

---

## Iteración 2 — V2 → V3

**Falla observada**

La segunda salida registraba correctamente temas, decisiones, acciones y pendientes, pero no destacaba cuáles requerían atención prioritaria ni ayudaba a visualizar riesgos, escenarios posibles o decisiones todavía pendientes.

**Pieza modificada:** 5. Formato.

**Cambio realizado**
- Se agregó un apartado de `Alertas y temas críticos`.
- Se incorporó un semáforo rojo / amarillo / verde.
- Para cada tema crítico se solicitó motivo de la alerta, escenarios posibles y decisión requerida.

**Qué cambió en la salida**
- La minuta comenzó a priorizar los asuntos críticos.
- Se visualizaron riesgos y escenarios.
- Se diferenciaron las decisiones ya tomadas de las decisiones todavía requeridas.

---

## Mejora adicional — V3 → V4

**Falla observada**

La tercera salida resultó excesivamente extensa y repetía información entre Resumen, Temas tratados, Próximas acciones, Temas pendientes y Alertas. Esto reducía la utilidad de la minuta como herramienta ejecutiva de lectura rápida.

**Pieza modificada:** 5. Formato.

**Cambio realizado**
- Se eliminó la tabla independiente de Temas tratados.
- Se eliminó la tabla independiente de Temas pendientes.
- El resumen pasó a tener entre 3 y 5 bullets.
- Las próximas acciones se limitaron a las más relevantes, con un máximo recomendado de 8.
- Las alertas se limitaron a 3–5 temas críticos.
- Se eliminó la columna Estado.
- `A completar antes de enviar` aparece solo cuando realmente existe un faltante importante.

**Qué cambió en la salida**
- Menor extensión y repetición.
- Mayor foco en decisiones, acciones y temas críticos.
- Formato más adecuado para una minuta que será enviada por correo.
