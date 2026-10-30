"""Revisión básica de Git sin imprimir valores sensibles. No sustituye una auditoría."""
import re
import subprocess
import sys


def git(*args):
    return subprocess.check_output(["git", *args], stderr=subprocess.DEVNULL)


try:
    commits = git("rev-list", "--all").decode().splitlines()
except (OSError, subprocess.CalledProcessError):
    print("Ejecute este script dentro de su repositorio Git local.")
    sys.exit(2)
patrones = [rb"gh[pousr]_[A-Za-z0-9]{25,}", rb"github_pat_[A-Za-z0-9_]{20,}",
            rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
            rb"(?im)^\s*(?:DB_PASSWORD|DJANGO_SECRET_KEY)\s*=\s*['\"]?(?!REEMPLAZAR|\$\{|os\.|required\(|$)[^\r\n]{8,}"]
revisados = set()
hallazgos = []
for commit in commits:
    for linea in git("ls-tree", "-r", "-z", commit).split(b"\0"):
        if not linea:
            continue
        meta, ruta = linea.split(b"\t", 1)
        modo, tipo, oid = meta.split()
        if tipo != b"blob":
            continue
        nombre = ruta.decode(errors="replace")
        if nombre.rsplit("/", 1)[-1] == ".env":
            hallazgos.append((commit[:10], nombre, "Archivo .env versionado"))
        if oid in revisados or nombre.endswith((".png", ".jpg", ".jpeg", ".pem")):
            continue
        revisados.add(oid)
        contenido = git("cat-file", "blob", oid.decode())
        if len(contenido) < 5_000_000 and any(re.search(p, contenido) for p in patrones):
            hallazgos.append((commit[:10], nombre, "Patrón a revisar; no se imprime el valor"))
print(f"Commits revisados: {len(commits)}. Objetos de texto examinados: {len(revisados)}.")
for commit, ruta, motivo in hallazgos:
    print(f"REVISAR: {commit} | {ruta} | {motivo}")
if hallazgos:
    print("Hay posibles hallazgos. Revise localmente antes de hacer público el repositorio.")
else:
    print("Sin coincidencias en esta revisión básica. Revise también capturas, datos y credenciales en otros formatos.")
sys.exit(1 if hallazgos else 0)
