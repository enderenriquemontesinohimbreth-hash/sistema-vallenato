# Pruebas de la Entrega 3

Actualización documental: 01/11/2026. Ejecución reportada: 30/10/2026.

## Resultado automatizado local

Entorno: Windows, Python 3.12, Django 5.2.18 y MySQL local. Servidor local 127.0.0.1:3305; base de pruebas aislada test_festival_web.
Se ejecutaron 39 pruebas: 24 heredadas y 15 nuevas, todas aprobadas en 11,649 segundos, con resultado OK.
Evidencia completa: [resultados_pruebas_e3.txt](../resultados_pruebas_e3.txt). Código nuevo: festival/tests_votos.py.
Los casos usan cuentas y datos ficticios creados en la base temporal; Django la elimina al finalizar.

| ID | Procedimiento | Resultado esperado | Resultado obtenido y estado | Prueba en la salida |
|---|---|---|---|---|
| CP-01 | Autenticar, elegir y confirmar opción válida | Un voto persistido | Aprobada; confirmación y persistencia verificadas | test_cp01_confirmacion_y_persistencia |
| CP-02 | Repetir con otra opción de otro subevento de la misma categoría | Mantener un solo voto | Aprobada; segundo intento rechazado | test_cp02_duplicado_otro_subevento |
| CP-03 | Votar en otra categoría con la misma cuenta | Permitir un voto en cada categoría | Aprobada | test_cp03_otra_categoria |
| CP-04 | Enviar sin sesión | Exigir autenticación y no guardar | Aprobada | test_cp04_sin_sesion |
| CP-05 | Cerrar entre selección y confirmación | Rechazar el envío final | Aprobada | test_cp05_cerrada_entre_seleccion_y_confirmacion |
| CP-06 | Enviar una opción de otra categoría | Rechazar y no guardar | Aprobada | test_cp06_opcion_ajena |
| CP-07 | Consultar historial con cuentas distintas | Cada cuenta ve solo sus votos | Aprobada | test_cp07_historial_personal |
| CP-08 | Consultar votos en Admin e intentar operaciones restringidas | Mostrar registros e impedir alta/borrado por Admin | Aprobada en automatización y consulta manual; comparación SQL independiente pendiente de documentar | test_cp08_admin_solo_consulta |
| CP-09 | Dos POST simultáneos con conexiones independientes y barrera | Exactamente un voto; respuestas controladas | Aprobada; un registro, éxito y duplicado | test_cp09_dos_post_simultaneos |
| CP-10 | Consultar GET /api/categorias/ y probar método no permitido | JSON con datos persistidos y colecciones vacías; POST 405 | Aprobada | test_cp10_api_mysql_y_vacios |

El caso CP-08 tiene evidencia de consulta administrativa y prueba automatizada, pero falta una captura de una consulta SQL directa para completar el contraste explícito con MySQL solicitado por la guía. No se presenta ese contraste independiente como ya realizado.

## Concurrencia y comprobaciones adicionales

CP-09 utiliza TransactionTestCase, dos clientes autenticados, conexiones independientes identificadas por CONNECTION_ID() y Barrier. Verifica un voto y respuestas de éxito y duplicado. Su ejecución local terminó en ok. Dos solicitudes no son una prueba de carga.
También se aprobaron unicidad SQL directa, otra edición, rechazo de edición incoherente y confirmación ausente, GET sin efectos, CSRF, votos y relaciones inmutables. Las 24 pruebas previas se ejecutaron de nuevo; no se heredó su aprobación sin ejecución.

## Comprobaciones manuales

El usuario confirmó localmente voto válido, duplicado, otra categoría, exigencia de sesión, categoría cerrada, historial, consulta administrativa y JSON. Confirmó además publicación y comprobaciones manuales en Azure de voto, duplicado, otra categoría, historial y API GET.
Las 39 pruebas NO se ejecutaron contra la base compartida de Azure. No atribuir al despliegue los resultados de la suite local.

## Evidencias por completar

- Incorporar capturas reales con su entorno (local o Azure), fecha y descripción.
- Documentar la consulta SQL de solo lectura de los votos y el contraste con Admin.
- Registrar los minutos reales del video una vez grabado, sin convertir tiempos propuestos en evidencia.
- Mantener pendientes las verificaciones no documentadas de contraste, teclado y tamaños de pantalla.
- No afirmar auditoría integral, carga masiva ni disponibilidad comprobadas.
