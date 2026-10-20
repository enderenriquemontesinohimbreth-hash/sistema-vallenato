"""Restaura la dependencia de presentación desde la distribución oficial."""
from pathlib import Path
from urllib.request import urlopen
import hashlib
BASE = Path(__file__).resolve().parent / 'static' / 'vendor'
BASE.mkdir(parents=True, exist_ok=True)
URL = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css'
# Se verifica integridad antes de escribir el archivo.
EXPECTED = 'd85327d99c7a3ee1f9b5d0500d1370acea3ad2db39c163c2f51f232baedbdede'
with urlopen(URL, timeout=30) as response:
    data = response.read()
if hashlib.sha256(data).hexdigest() != EXPECTED:
    raise RuntimeError('El recurso no coincide con la versión revisada.')
(BASE / 'bootstrap.min.css').write_bytes(data)
license_url = 'https://raw.githubusercontent.com/twbs/bootstrap/v5.3.8/LICENSE'
with urlopen(license_url, timeout=30) as response:
    (BASE / 'BOOTSTRAP_LICENSE.txt').write_bytes(response.read())
print('Bootstrap 5.3.8 y licencia disponibles localmente.')
