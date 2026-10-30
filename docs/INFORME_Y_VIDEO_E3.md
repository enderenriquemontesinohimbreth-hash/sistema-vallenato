# Borrador académico para completar con evidencias reales

## 1. Portada
Fundación Universitaria del Área Andina. [Programa académico]. Desarrollo Web.
Sistema Web de Votaciones — Festival de la Leyenda Vallenata 2027. Entrega 3.
Docente: [Nombre]. Cinco integrantes: [Nombre 1], [Nombre 2], [Nombre 3], [Nombre 4], [Nombre 5].
Composición de cinco según autorización informada por el estudiante; la guía indica cuatro.
Fecha: [Fecha del envío]. Un único PDF, cargado individualmente por los integrantes.

## 2. Ficha de acceso, inmediatamente después de portada
| Elemento | Información |
|---|---|
| Repositorio | https://github.com/enderenriquemontesinohimbreth-hash/sistema-vallenato — visibilidad pública pendiente |
| README | https://github.com/enderenriquemontesinohimbreth-hash/sistema-vallenato/blob/main/README.md — verificar versión publicada |
| API | /api/categorias/ — festival/views.py, api_categorias — [minuto real] |
| Unicidad | festival/models.py, Voto.Meta; festival/services.py — [minuto real] |
| Video | [Enlace real], [duración real, máximo 8 minutos] |
| Aplicación | https://vallenato-ender-2027-gfgdgzewbyhuhedj.canadacentral-01.azurewebsites.net/ — actualización E3 pendiente |
| Minutos | Login [ ]; voto [ ]; duplicado [ ]; otra categoría [ ]; historial [ ]; API [ ]; MySQL [ ] |

## 3. Introducción y objetivo
La tercera fase amplía el catálogo Django y MySQL con un módulo de votación sujeto a una elección por usuario, categoría y edición. La propuesta integra selección, confirmación, validación del servidor, consulta de participación y una API GET. Esta primera versión contiene código y migraciones generadas; su funcionamiento persistido debe comprobarse en MySQL antes de describirse como implementado y verificado en el informe final.
Objetivo general: desarrollar y verificar un módulo de votaciones integrado al proyecto existente, con unicidad por usuario, categoría y edición, consulta de participación y API GET respaldadas por MySQL.

## 4. Implementación técnica
Incorporar la explicación de MODELO_Y_API_E3.md y el diagrama. Distinguir reglas obligatorias de propuestas: habilitación manual, cierre inicial de categorías, votos sin edición/borrado administrativo y relaciones padre inmutables son decisiones técnicas de esta versión.
[Insertar captura real de migración aplicada y esquema MySQL].

## 5. Funcionalidades
[Captura real de selección]. [Captura real de confirmación]. [Captura real de voto persistido]. [Captura real de bloqueo duplicado]. [Captura real de Mi participación]. [Captura real de Admin]. [Captura real de JSON].
No utilizar páginas renderizadas para revisión visual como evidencia de persistencia.

## 6. Pruebas
Completar la matriz de PRUEBAS_ENTREGA_3.md con resultados reales y fechas. No heredar aprobaciones de la Entrega 2.

## 7. Conclusiones y equipo
Borrador: el diseño conecta el voto con el catálogo previo y centraliza la unicidad a nivel de categoría. La restricción SQL y las transacciones ofrecen una estrategia verificable ante duplicados. La conclusión sobre su eficacia depende de las pruebas aún pendientes en MySQL. Persisten pendientes de actualización, evidencias, revisión docente y publicación de materiales.

| Integrante | Responsabilidad propuesta | Aporte realizado y evidencia |
|---|---|---|
| [Nombre 1] | Coordinación e integración | Pendiente de registrar |
| [Nombre 2] | Modelos y MySQL | Pendiente de registrar |
| [Nombre 3] | Vistas y validaciones | Pendiente de registrar |
| [Nombre 4] | Interfaz y API | Pendiente de registrar |
| [Nombre 5] | Pruebas y documentación | Pendiente de registrar |

## Guion de video propuesto (máximo 8 minutos)
Puede sustentar un delegado o todo el equipo, según la guía. No es obligatorio que todos hablen.
0:00–0:45: presentar equipo, alcance y datos ficticios.
0:45–1:30: mostrar login y categorías consultadas.
1:30–2:30: seleccionar, confirmar, registrar y mostrar el voto.
2:30–3:30: intentar otra opción de otro subevento en la misma categoría; mostrar bloqueo.
3:30–4:15: registrar en otra categoría.
4:15–5:00: mostrar historial propio y Admin.
5:00–6:00: consultar API y explicar categorías/opciones desde MySQL.
6:00–7:00: mostrar fila SQL, migración y UniqueConstraint.
7:00–8:00: explicar pruebas, concurrencia documentada y límites.
Estas marcas son orientativas: sustituir por tiempos reales tras grabar. CP que no aparezca necesita evidencia adicional clara en PDF. No mostrar secretos en pantalla.

## Matriz de rúbrica
| Criterio | Puntos de guía | Producto | Estado real |
|---|---:|---|---|
| Modelo e integración | 4 | Modelo y 0002 | Código generado; aplicación MySQL pendiente |
| Votaciones y API GET | 6 | Vistas, formularios, historial y API | Código generado; ejecución funcional pendiente |
| Validaciones y seguridad | 5 | Servicio, CSRF, permisos, unicidad | Código generado; CP pendientes |
| Pruebas/evidencias/documentación | 5 | Tests y borradores | Parcial; sin video/PDF final ni resultados nuevos |
No se asigna calificación.

## Cronograma propuesto
30 oct–1 nov: integrar y aplicar migración en desarrollo; revisar diseño.
2–4 nov: ejecutar CP-01 a CP-10 y regresión, corregir hallazgos.
5–6 nov: actualizar Azure y verificar enlaces/privacidad.
7–8 nov: grabar video máximo 8 min, incorporar capturas/resultados y exportar PDF.
9 nov: verificar PDF descargado, enlaces en incógnito y envíos individuales antes de 23:59.
Observaciones específicas de la Entrega 2: pendientes de recibir.
