import csv
from pathlib import Path
from urllib.parse import quote

OWNER = "Aztirma"
REPO = "Datamind"
BRANCH = "main"
FOLDER = "Imagenes"

repo_root = Path(r"C:\Proyectos\Datamind")
img_dir = repo_root / FOLDER

# Busca imágenes reales en disco (png/jpg/jpeg)
exts = {".png", ".jpg", ".jpeg"}
files = sorted([p for p in img_dir.rglob("*") if p.is_file() and p.suffix.lower() in exts])

rows = []
for p in files:
    rel_path = p.relative_to(repo_root).as_posix()  # Imagenes/archivo.png
    rel_path_clean = rel_path.strip().strip('"')    # por si hubiera comillas pegadas
    url_path = quote(rel_path_clean)                # encodea espacios/tildes
    raw_url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{url_path}"
    rows.append((p.name, raw_url))

out_csv = repo_root / "imagenes_urls.csv"
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["NombreArchivo", "ImageURL"])
    w.writerows(rows)

print(f"Listo: {out_csv} ({len(rows)} URLs)")
