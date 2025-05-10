# stl_loader.py

from stl import mesh

def load_stl(file_path: str) -> mesh.Mesh:
    print(f"📂 Chargement du fichier STL : {file_path}")
    return mesh.Mesh.from_file(file_path)
