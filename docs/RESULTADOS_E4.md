# Resultados acumulados de la Entrega 4

Actualización de verificación local del 15/11/2026: las siete pruebas del módulo de resultados fueron aprobadas en 0,747 segundos. La suite completa terminó con 46 pruebas aprobadas en 17,208 segundos y resultado OK. También se comprobó manualmente que un nuevo voto aumenta exactamente en uno el conteo de la opción y de su categoría. Evidencia automatizada: resultados_pruebas_e4.txt. La publicación y verificación de esta función en Azure siguen pendientes.

## Alcance propuesto y funcionamiento

Nueva consulta GET /resultados/, pública, de solo lectura y sin datos personales. Presenta votos por opción/subevento, total por categoría y total de votos en las categorías mostradas. Ese último total no representa personas únicas, porque una persona puede votar en varias categorías.
Permite elegir edición y filtrar una categoría de esa edición. Incluye opciones con cero votos y estados sin ediciones, sin categorías, sin opciones y sin votos. Las categorías cerradas conservan resultados. Los empates se muestran con el mismo conteo y orden por nombre; no se declara ganador.
La consulta cuenta los registros actuales de Voto mediante Opcion.objects.annotate(total_votos=Count("votos")). No duplica ni guarda un contador. Un nuevo voto se refleja al volver a consultar; no se implementa actualización automática.
La propuesta académica muestra acumulados de categorías abiertas como provisionales. Esta decisión no implica aprobación de una política oficial del Festival. La API /api/categorias/ conserva su contrato y no publica votos individuales ni resultados.

## Archivos

- festival/resultados.py: vista, filtros validados, conteo ORM y respuesta sin caché.
- festival/urls.py: ruta resultados/.
- templates/festival/resultados.html: filtros y tablas accesibles.
- templates/base.html: enlace Resultados.
- templates/festival/votaciones.html: enlace a resultados de la categoría.
- festival/tests_resultados.py: siete pruebas de integración previstas sobre MySQL.

No cambian modelos, esquema, dependencias, credenciales ni reglas del voto. No se requiere una nueva migración. El almacenamiento existente se conserva.

## Aplicación local paso a paso

1. Guardar cambios propios antes de actualizar; no descartar archivos con reset --hard.
2. En la carpeta que contiene manage.py, ejecutar git status. Si está limpio, git switch main y git pull --ff-only origin main.
3. Crear la rama: git switch -c entrega-4-resultados.
4. Extraer ACTUALIZACION_RESULTADOS_E4.zip y copiar su contenido en la raíz del proyecto, aceptando reemplazar solo los archivos incluidos. Conservar .env y .venv.
5. Confirmar que la configuración apunta a MySQL LOCAL, no Azure:

```powershell
.\.venv\Scripts\python.exe manage.py shell -c "from django.conf import settings; db=settings.DATABASES['default']; print('Servidor:', db['HOST']); print('Puerto:', db['PORT']); print('Base:', db['NAME'])"
```

En el computador de Ender: servidor 127.0.0.1, puerto 3305 y base festival_web. No se necesitan nuevas credenciales.

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test festival.tests_resultados --verbosity 2
.\.venv\Scripts\python.exe manage.py test --verbosity 2 2>&1 | Tee-Object -FilePath resultados_pruebas_e4.txt
.\.venv\Scripts\python.exe manage.py collectstatic --noinput
.\.venv\Scripts\python.exe manage.py runserver
```

La prueba aislada debe encontrar siete casos. Si la versión anterior mantiene 39 pruebas sin cambios, la suite completa debería encontrar 46; es una previsión, no un resultado ejecutado. Si alguna falla, conservar el error para corregirlo. No marcarla como aprobada por tener código.
Las pruebas crean y eliminan una base temporal. No ejecutarlas contra la base compartida de Azure. El servidor runserver no es necesario para ejecutar tests.

Abrir http://127.0.0.1:8000/resultados/ o el nuevo menú Resultados. Probar:

1. Seleccionar edición y pulsar Ver edición.
2. Elegir categoría y pulsar Filtrar categoría.
3. Comparar sus conteos con MySQL.
4. Registrar un voto permitido desde una cuenta de prueba nueva, volver y recargar Resultados: solo la opción elegida debe aumentar en uno.
5. Intentar un duplicado: el total no debe aumentar.
6. Comprobar ceros, categorías cerradas y otra edición.
7. Verificar en celular y mediante teclado; no se da por completada esa inspección visual aquí.

## Pruebas nuevas y estado real

| Prueba | Verificación | Estado en el entorno de preparación |
|---|---|---|
| Conteos, ceros y privacidad | Total 1 y opción cero; sin usuario; no-store | No ejecutada en MySQL |
| Separación | Filtra categoría y edición; total no cuenta usuarios únicos | No ejecutada en MySQL |
| Filtros inválidos | 400 por entrada inválida y 404 por relación incoherente | No ejecutada en MySQL |
| Categoría cerrada | Conserva conteo ya registrado | No ejecutada en MySQL |
| Actualización y duplicados | Nuevo voto suma uno; duplicado no suma | No ejecutada en MySQL |
| Solo lectura | GET no crea votos y POST devuelve 405 | No ejecutada en MySQL |
| Estados vacíos | Sin edición, categoría, opciones o votos | No ejecutada en MySQL |

Se verificaron sintaxis Python, compilación de plantillas y Django check sin incidencias con un controlador auxiliar temporal PyMySQL solo para análisis. No se reemplazó mysqlclient en el proyecto. Se comprobó render con datos simulados, rechazo de POST y entradas inválidas sin MySQL. No se ejecutaron aquí el conteo SQL ni las siete pruebas de integración por ausencia de servidor MySQL.
Los 39 resultados aprobados anteriores siguen siendo evidencia de la versión anterior, no de esta actualización.

## Consulta SQL de contraste solo lectura

Conectarse a la base correspondiente a la interfaz que se está revisando: local con local o Azure con Azure. Los datos no son compartidos entre ambas.

```sql
USE festival_web;
SELECT
    e.anio AS edicion,
    c.id AS categoria_id,
    c.nombre AS categoria,
    s.titulo AS subevento,
    o.id AS opcion_id,
    o.nombre AS opcion,
    COUNT(v.id) AS total_votos
FROM festival_opcion AS o
JOIN festival_votacion AS s ON s.id = o.votacion_id
JOIN festival_categoria AS c ON c.id = s.categoria_id
JOIN festival_edicion AS e ON e.id = c.edicion_id
LEFT JOIN festival_voto AS v ON v.opcion_id = o.id
GROUP BY e.anio, c.id, c.nombre, s.titulo, o.id, o.nombre
ORDER BY e.anio DESC, c.id, total_votos DESC, o.nombre, o.id;
```

El LEFT JOIN conserva las opciones que no recibieron votos. Comparar números con la misma edición y categoría de la página. Esta consulta no modifica registros.

## Publicación después de las pruebas

Revisar git diff --stat, guardar los ocho archivos del paquete y publicar entrega-4-resultados. Crear una solicitud de integración a main; revisar y completar la integración cuando las pruebas estén aprobadas. Main activa GitHub Actions. No detener ni migrar MySQL por esta actualización, porque no cambia el esquema.
No se ha modificado GitHub ni Azure desde el entorno de preparación. La nueva dirección pública /resultados/ solo funcionará después del despliegue exitoso. Verificar Actions y repetir la comparación en el entorno publicado.

## Preparación de la sustentación

Mostrar resultados, registrar un voto con una cuenta nueva y recargar para comprobar el aumento. Mostrar SQL equivalente y explicar Count. Repetir CP-06 y CP-09 con los comandos ya indicados; el módulo de conteo no cambia sus reglas. Conservar evidencias nuevas y actualizar la documentación con resultados reales.

Fuente técnica: Django Software Foundation, Aggregation, Django 5.2. https://docs.djangoproject.com/en/5.2/topics/db/aggregation/ (consulta 15/11/2026).
