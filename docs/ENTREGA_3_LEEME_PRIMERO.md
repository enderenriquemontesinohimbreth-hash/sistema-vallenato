# Entrega 3: primera versión de trabajo

Esta copia parte del ZIP sistema-vallenato-main recibido el 30 de octubre de 2026.
No fue publicada en GitHub ni Azure. No cambia la visibilidad de su repositorio.

## Qué se agregó

- Categoría.habilitada (False por defecto): abra el administrador y habilite explícitamente las categorías que pueden recibir votos.
- Voto con usuario, categoría, opción y fecha. La edición se obtiene por categoría.edicion.
- Unicidad SQL usuario+categoría: categoría pertenece a una única edición y no puede trasladarse. Garantiza un voto por categoría y edición, incluidos sus subeventos.
- Selección y confirmación por POST/CSRF; historial privado; consulta administrativa solo lectura.
- GET /api/categorias/ (público, sin votos individuales ni datos de usuarios).
- Fotografía histórica de fondo, adaptación visual y créditos.

## Antes de actualizar (Windows)

1. Conserve su carpeta original, sus credenciales y la versión entregada en el Eje 2.
2. Revise `git status` y cree una rama de trabajo: `git switch -c entrega-3`.
3. Copie los archivos de `CAMBIOS_ENTREGA_3.zip` sobre la raíz que contiene manage.py. El paquete no contiene .env ni .venv.
4. No cambie DB_HOST a Azure para las pruebas. Use una base LOCAL de desarrollo y una base temporal de pruebas.
5. No ejecute `git push origin main` hasta comprobar esta versión: main activa el despliegue.

## Comandos iniciales, uno por uno, en PowerShell

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py showmigrations festival
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py cargar_demo_e3
.\.venv\Scripts\python.exe manage.py test --verbosity 2 2>&1 | Tee-Object -FilePath resultados_pruebas_e3.txt
.\.venv\Scripts\python.exe manage.py collectstatic --noinput
.\.venv\Scripts\python.exe manage.py runserver
```

No hace falta volver a ejecutar makemigrations: la migración 0002 está incluida. Use `makemigrations --check --dry-run` para detectar desajustes.
El usuario de desarrollo necesita permisos para crear y eliminar SOLO la base temporal test_<DB_NAME>. No amplíe por este motivo los permisos del usuario de Azure.

## Recorrido local

- http://127.0.0.1:8000/ : inicio.
- http://127.0.0.1:8000/admin/ : habilitar categorías y consultar votos.
- http://127.0.0.1:8000/mi-participacion/ : historial propio (requiere sesión).
- http://127.0.0.1:8000/api/categorias/ : API GET.
- Catálogo → edición → categoría → Participar → seleccionar opción → revisar → marcar confirmación → registrar.
- Los distintos subeventos de una categoría comparten la misma selección y límite.

No se crean usuarios ni contraseñas nuevas automáticamente. Use cuentas de prueba propias.

## Actualizar Azure, después de validar localmente

1. Respalde la base y registre la versión anterior del código.
2. Mantenga la aplicación detenida durante la actualización de esquema y código (ventana de mantenimiento).
3. Aplique únicamente `migrate` a la base de Azure mediante el procedimiento seguro de conexión ya configurado; confirme el nombre del servidor antes de ejecutarlo.
4. Integre la rama revisada en main; GitHub Actions publicará el código. No copie .env ni credenciales a GitHub.
5. Verifique collectstatic y arranque; reanude la aplicación.
6. Compruebe navegación, un voto de prueba, duplicado, otra categoría y API pública. Los ejemplos no se cargan automáticamente en Azure.
7. La migración es aditiva. No revierta 0002 si contiene votos: su reversión elimina el modelo Voto y pierde esos registros.

La política provisional impide modificar o borrar votos desde Admin. No permite cambiar el padre de una categoría, subevento u opción existente; cree registros nuevos. Operaciones SQL manuales, QuerySet.update y bulk_create omiten validaciones del modelo: no se ofrecen como vías de edición del catálogo. La restricción SQL de unicidad sí protege duplicados incluso con inserciones directas.

## Estado real

El código fue escrito y las plantillas compiladas. Se generó la migración y Django check no reportó problemas usando un controlador auxiliar temporal en el entorno de revisión. No se cambió el controlador mysqlclient del proyecto entregado.
No hubo un servidor MySQL disponible aquí: migraciones aplicadas, pruebas funcionales, integridad concurrente y regresión permanecen NO EJECUTADAS/BLOQUEADAS. La advertencia al generar migraciones indica que no pudo comprobarse el historial contra MySQL.
Los resultados de 24 pruebas anteriores pertenecen a la Entrega 2, no validan la Entrega 3.

## Publicación del repositorio

Su autorización para hacerlo público está registrada. El ZIP no incluye el historial Git ni permite modificar GitHub remotamente. La revisión básica no detectó .env real, tokens de GitHub ni claves privadas en los archivos de texto recibidos; no es una auditoría completa.
Antes del cambio ejecute en su repositorio local `.\.venv\Scripts\python.exe tools/revisar_historial.py` y revise las capturas. El script revisa patrones básicos e imprime solo archivos y commits, no valores; no es una certificación de ausencia de secretos. No comparta el archivo .env ni el resultado de una búsqueda que muestre claves.
Tras esa revisión: GitHub → sistema-vallenato → Settings → General → Danger Zone → Change repository visibility → Change to public; siga la confirmación. Verifique el enlace en incógnito.
No se ha cambiado todavía la visibilidad. No necesita volver a autorizar el cambio; falta acceso y revisión del historial.

La comprobación visual en navegador quedó pendiente: el navegador de pruebas no pudo descargarse. La compilación HTML sí se realizó, pero no demuestra adaptación responsive ni contraste comprobado.
