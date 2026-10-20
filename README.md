# Sistema de votaciones del Festival 2027 — Entrega 2

Aplicación académica Django MVT con MySQL. Permite consultar ediciones, categorías,
votaciones y opciones, crear cuentas e iniciar/cerrar sesión. El catálogo se administra
con Django Admin. No registra votos, resultados ni políticas de elegibilidad.

## Equipo
[Integrante 1], [Integrante 2], [Integrante 3], [Integrante 4], [Integrante 5].
Cinco integrantes autorizados por el docente, según información del solicitante.
El equipo debe completar los nombres y demostrar su participación.

## Versiones
Verificado en Python 3.12.14, Django 5.2.18, mysqlclient 2.2.7,
python-dotenv 1.2.1 y MySQL 8.0.46 en Ubuntu 24.04. Bootstrap 5.3.8 se sirve localmente.
Para Windows se propone Python 3.12 de 64 bits y MySQL Community Server 8.4 LTS.
La instalación en Windows y MySQL 8.4 debe verificarse en los equipos del grupo.
Django 5.2 admite Python 3.10–3.14 y MySQL >=8.0.11 según documentación oficial.
Use versiones vigentes compatibles y repita las pruebas si cambia las fijadas.

## Instalación inicial en Windows PowerShell

Instale Python 3.12 de 64 bits, MySQL Community Server y el cliente mysql.
Descomprima el proyecto y sitúese en la carpeta que contiene manage.py.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copie la clave generada únicamente en DJANGO_SECRET_KEY de .env.
Edite DB_PASSWORD con una contraseña local propia. No entregue .env.
Si la política de PowerShell impide activar el entorno, no es necesario cambiarla:
use .\.venv\Scripts\python.exe en lugar de python en cada comando.
Si mysql no está en PATH, invoque su ruta completa de instalación.

Abra el cliente con `mysql -u root -p`. El usuario administrador de MySQL se usa
solo para aprovisionar; la aplicación usa festival_app.
Ejecute el siguiente SQL sustituyendo las contraseñas de ejemplo localmente:

```sql
CREATE DATABASE festival_web
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
CREATE USER 'festival_app'@'127.0.0.1'
  IDENTIFIED BY 'REEMPLAZAR_LOCALMENTE';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX, DROP, REFERENCES
  ON festival_web.* TO 'festival_app'@'127.0.0.1';
-- Solo para ejecutar pruebas: alcance limitado a la base de pruebas.
GRANT ALL PRIVILEGES ON test_festival_web.*
  TO 'festival_app'@'127.0.0.1';
```

No utilice literalmente la contraseña de ejemplo. DB_HOST debe ser 127.0.0.1
para coincidir con el usuario aprovisionado. Ajuste DB_PORT si MySQL no usa 3306.
Los privilegios DDL se requieren para migraciones locales; en producción se deben
separar los usuarios de migración y ejecución. No se configura producción aquí.
No cree manualmente test_festival_web: Django la crea y elimina durante las pruebas.

```powershell
python manage.py migrate
python manage.py showmigrations festival
python manage.py check --database default
python manage.py createsuperuser
python manage.py cargar_demo
python manage.py runserver
```

Abra http://127.0.0.1:8000/ y http://127.0.0.1:8000/admin/.
Las credenciales se crean localmente. No se entregan usuarios con contraseña fija.
Bootstrap ya está incluido; para restaurarlo ejecute `python descargar_bootstrap.py`.
Ese comando requiere internet y comprueba el SHA-256 del CSS.

## Instalación en Linux o macOS

En Ubuntu, instale previamente python3-venv, python3-dev, build-essential,
pkg-config y default-libmysqlclient-dev. Instale MySQL Server por el procedimiento
oficial de su sistema. En macOS configure las bibliotecas cliente y pkg-config
según las instrucciones de mysqlclient. Después:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Complete .env, aprovisione MySQL y ejecute los mismos comandos manage.py.
Si mysqlclient falla al compilar, compruebe compilador, cabeceras de Python,
bibliotecas de MySQL y pkg-config. No sustituya el backend por SQLite.

## Uso habitual

Active el entorno, confirme que el servicio MySQL esté iniciado y ejecute:

```powershell
python manage.py runserver
```

No repita CREATE DATABASE, CREATE USER o createsuperuser en cada inicio.
El comando cargar_demo es idempotente respecto de sus claves: no duplica registros
ni sobrescribe los existentes. En una base vacía crea 2 ediciones, 4 categorías,
4 votaciones y 8 opciones. Todo su contenido es ficticio.

## Administración y navegación

Con el superusuario ingrese a /admin/. Cree edición, categoría, votación y opción
en ese orden. Abra el catálogo público para verificar los cambios. Los enlaces
anidados validan edición, categoría y votación en la consulta del servidor.
La consulta del catálogo es pública; el registro crea usuarios sin permisos staff.
El cierre de sesión es un formulario POST protegido con CSRF.
Las relaciones usan PROTECT: no puede eliminar un padre con hijos existentes.
La identidad, la frecuencia y la elegibilidad del futuro voto siguen pendientes.

## Pruebas

```powershell
python manage.py test --verbosity 2
python manage.py makemigrations --check --dry-run
```

Las 24 pruebas incluidas usan el backend MySQL y una base separada test_festival_web.
Una prueba rechaza explícitamente SQLite y MariaDB para evidenciar MySQL real.
Use un servidor de desarrollo propio, no datos de producción. La cuenta requiere
permisos sobre la base de pruebas; no necesita privilegios globales.
Para inspección visual pruebe inicio, detalle y registro en 360, 768 y 1280 px;
revise teclado, errores, estados vacíos y coherencia de navegación.

## Estructura

- config/: configuración, URLs principales y WSGI.
- festival/: modelos, Admin, vistas, URLs, pruebas y comando cargar_demo.
- cuentas/: formulario, vista de registro, rutas de autenticación y pruebas.
- templates/: base, catálogo, autenticación y página 404.
- static/: CSS y JavaScript propios, Bootstrap y licencia.
- evidencias/: logs sanitizados, resultados y capturas de la verificación local.
- docs/: guion y plan de cierre.

## Estado y entrega

Implementación y verificación local disponibles. No hay despliegue de producción.
Repositorio: [Enlace real del repositorio]. Video: [Enlace real del video].
Publicación y verificación de permisos pendientes a cargo del equipo.
La entrega oficial es un único PDF con evidencias y enlaces clicables, hasta el
26 de octubre de 2026. El Word es el original editable y debe completarse con
nombres, enlaces y participación real antes de exportar la versión definitiva.
No se adjunta la base de datos ni .env. Se reconstruyen con migraciones y cargar_demo.

## Recursos y fuentes

Bootstrap 5.3.8: copyright de sus autores, licencia MIT incluida en static/vendor.
No se usan imágenes, logotipos ni identidad institucional.
Código específico del proyecto: material académico; la licencia de publicación
queda por decidir por el equipo antes de subirlo a un repositorio.
Fuentes oficiales consultadas el 19/10/2026:
- https://docs.djangoproject.com/en/5.2/faq/install/
- https://docs.djangoproject.com/en/5.2/ref/databases/
- https://docs.djangoproject.com/en/5.2/topics/auth/default/
- https://docs.djangoproject.com/en/5.2/ref/contrib/admin/
- https://docs.djangoproject.com/en/5.2/topics/testing/overview/
- https://www.djangoproject.com/weblog/2026/oct/06/security-releases/
- https://dev.mysql.com/doc/refman/8.4/en/installing.html
- https://pypi.org/project/mysqlclient/
- https://pypi.org/project/python-dotenv/
- https://getbootstrap.com/docs/5.3/getting-started/download/
