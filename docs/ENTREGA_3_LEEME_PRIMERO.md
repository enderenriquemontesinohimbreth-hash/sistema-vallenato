# Entrega 3: instrucciones y estado de verificación

Esta copia parte del ZIP sistema-vallenato-main recibido el 30 de octubre de 2026.
Posteriormente se publicó la rama entrega-3 y se integró la actualización en main.
La aplicación de Azure fue actualizada y el usuario confirmó que el repositorio abre públicamente en incógnito.
Estado de documentación actualizado el 01/11/2026 con las verificaciones reportadas el 30/10/2026.

## Qué se agregó

- Categoría.habilitada (False por defecto): abra el administrador y habilite explícitamente las categorías que pueden recibir votos.
- Voto con usuario, categoría, opción y fecha. La edición se obtiene por categoría.edicion.
- Unicidad SQL usuario+categoría: categoría pertenece a una única edición y no puede trasladarse. Garantiza un voto por categoría y edición, incluidos sus subeventos.
- Selección y confirmación por POST/CSRF; historial privado; consulta administrativa solo lectura.
- GET /api/categorias/ (público, sin votos individuales ni datos de usuarios).
- Fotografía histórica de fondo, adaptación visual y créditos.

## Procedimiento para futuras actualizaciones en Windows

1. Conserve su carpeta original, sus credenciales y la versión entregada en el Eje 2.
2. Revise `git status`, sincronice main si el árbol está limpio y cree una rama nueva para el cambio. La rama entrega-3 ya se utilizó.
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

- Migración festival.0002_categoria_habilitada_voto aplicada con OK en MySQL local y Azure.
- Suite local: 39 pruebas aprobadas (24 heredadas y 15 nuevas), 11,649 segundos, resultado OK. Incluye la prueba de dos POST simultáneos y conexiones independientes.
- Evidencia de la ejecución local: resultados_pruebas_e3.txt.
- El usuario confirmó la nueva presentación y comprobaciones manuales en Azure: voto registrado, duplicado rechazado, participación en otra categoría e información de la API.
- No se ejecutó la suite contra MySQL compartido de Azure. Los datos locales no se transfieren automáticamente a Azure.
- La evidencia visual fue tomada por el equipo; falta incorporarla al informe final. La comparación directa de votos con SQL sigue pendiente de documentar.
- Pendientes: revisión completa de tamaños de pantalla, teclado y contraste, video, marcas reales, aportes individuales y PDF final. La navegación manual no certifica toda la accesibilidad.

## Publicación del repositorio

El usuario ejecutó tools/revisar_historial.py: 4 commits y 52 objetos examinados, sin coincidencias en los patrones básicos. No es una auditoría exhaustiva de secretos ni un análisis del contenido de imágenes.
El repositorio se cambió a público y el usuario confirmó la lectura sin sesión desde incógnito.
No subir .env real, contraseñas, tokens ni claves privadas. Repetir la revisión antes de futuras publicaciones y comprobar las capturas.

## Alcance de los resultados

Las primeras comprobaciones de preparación se hicieron sin MySQL en el entorno de generación del código. Ese estado histórico fue superado por la ejecución posterior en el computador del equipo. Las 39 pruebas aprobadas documentan ese entorno local; no se atribuyen al entorno inicial ni al despliegue de Azure.
No se han verificado carga masiva, disponibilidad garantizada ni seguridad integral.
