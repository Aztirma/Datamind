import csv
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote
import glob

OWNER = "Aztirma"
REPO = "Datamind"
BRANCH = "main"
FOLDER = "Imagenes"  # carpeta del repo

def find_git_exe() -> str:
    # 1) si estuviera en PATH
    p = shutil.which("git")
    if p:
        return p

    # 2) GitHub Desktop (ruta variable por versión)
    pattern = r"C:\Users\alejandra.zuniga\AppData\Local\GitHubDesktop\app-*\resources\app\git\cmd\git.exe"
    matches = sorted(glob.glob(pattern))
    if matches:
        return matches[-1]  # el más reciente

    raise FileNotFoundError(
        "No encontré git.exe. Abre GitHub Desktop y asegúrate de que esté instalado correctamente."
    )

def main():
    repo_root = Path(r"C:\Proyectos\Datamind")
    git_exe = find_git_exe()

    cmd = [git_exe, "ls-files", f"{FOLDER}/"]
    res = subprocess.run(
        cmd,
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=True
    )

    files = [line.strip() for line in res.stdout.splitlines() if line.strip()]

    rows = []
    for rel_path in files:
        url_path = quote(rel_path)  # encodea espacios/tildes
        raw_url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{url_path}"
        name = Path(rel_path).name
        rows.append((name, raw_url))

    out_csv = repo_root / "imagenes_urls.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["NombreArchivo", "ImageURL"])
        w.writerows(rows)

    print(f"Listo: {out_csv} ({len(rows)} URLs)")

if __name__ == "__main__":
    main()
