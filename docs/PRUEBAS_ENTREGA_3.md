# Matriz CP-01 a CP-10 — pendiente de ejecución en MySQL

Actualización de verificación local: se aplicó correctamente la migración festival.0002_categoria_habilitada_voto en MySQL local. La ejecución automatizada finalizó con 39 pruebas aprobadas en 11,649 segundos y resultado “OK”, incluida la prueba de dos solicitudes simultáneas. Evidencia: resultados_pruebas_e3.txt. La verificación de esta versión en Azure permanece pendiente.

| ID | Procedimiento | Resultado esperado | Resultado obtenido / estado | Evidencia |
|---|---|---|---|---|
| CP-01 | Autenticar, seleccionar y confirmar opción | Un voto persistido | No ejecutada: sin MySQL en entorno de revisión | Pendiente |
| CP-02 | Repetir en misma categoría con otra opción y subevento | Mantiene un solo voto | No ejecutada | Pendiente |
| CP-03 | Participar en otra categoría | Un voto en cada categoría | No ejecutada | Pendiente |
| CP-04 | Enviar sin sesión | Exige autenticación, cero votos | No ejecutada | Pendiente |
| CP-05 | Cerrar categoría después de seleccionar y confirmar | Rechaza registro | No ejecutada | Pendiente |
| CP-06 | Manipular opción de otra categoría | Rechaza registro | No ejecutada | Pendiente |
| CP-07 | Abrir Mi participación con dos usuarios | Cada uno ve solo sus votos | No ejecutada | Pendiente |
| CP-08 | Consultar Admin y comparar SQL | Datos coinciden; no permite edición de votos | No ejecutada | Pendiente |
| CP-09 | Dos POST en hilos y conexiones independientes con barrera | Un voto y respuesta controlada para ambos | No ejecutada | Pendiente |
| CP-10 | GET /api/categorias/ | JSON válido con datos persistidos y categorías vacías | No ejecutada | Pendiente |

Implementación: festival/tests_votos.py. CP-09 usa TransactionTestCase, dos clientes autenticados, conexiones independientes verificadas por CONNECTION_ID() y sincronización con Barrier; no se sustituye por llamadas secuenciales. Su ejecución sigue pendiente.
Pruebas adicionales: CSRF, GET sin efectos, confirmación obligatoria, edición incoherente, unicidad SQL directa, inmutabilidad, edición distinta e historial aislado. Las 24 pruebas heredadas siguen incluidas sin marcar nuevas aprobaciones.

## Comprobaciones efectuadas aquí

- Sintaxis Python y compilación de plantillas: efectuadas sin acceso a datos.
- Django check: sin incidencias usando controlador auxiliar PyMySQL solo para análisis; mysqlclient del proyecto no se reemplazó.
- Generación de 0002 y detección de cambios: no hay cambios de modelos sin migración. Historial real pendiente por ausencia de conexión MySQL.
- Las páginas para inspección visual usan objetos ficticios en memoria exclusivamente para renderizar plantillas. No prueban vistas/POST/MySQL.

Complete fecha, entorno, resultado observado, archivo de evidencia y minuto REAL del video tras cada ejecución. Nunca reutilice marcas de video propuestas como si fueran reales.

Revisión visual en navegador: bloqueada por descarga fallida del navegador de pruebas. Mobile/desktop, contraste y teclado quedan pendientes.
