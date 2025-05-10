# slicer_core.py

import numpy as np
from stl import mesh
from typing import List, Tuple

def slice_model(
    mesh_obj: mesh.Mesh,
    layer_height: float = 0.2
) -> List[List[Tuple[np.ndarray, np.ndarray]]]:
    """
    Découpe le modèle STL en tranches horizontales et retourne les segments 2D.
    """
    z_min = float(np.min(mesh_obj.z))
    z_max = float(np.max(mesh_obj.z))
    print(f"📐 Tranchage du modèle : Z min = {z_min:.2f}, Z max = {z_max:.2f}")

    layers = np.arange(z_min, z_max + layer_height, layer_height)
    print(f"🧱 Nombre total de couches : {len(layers)}")

    all_segments: List[List[Tuple[np.ndarray, np.ndarray]]] = []

    for z in layers:
        segments: List[Tuple[np.ndarray, np.ndarray]] = []

        for triangle in mesh_obj.vectors:
            intersections: List[np.ndarray] = []

            for j in range(3):
                p1 = triangle[j]
                p2 = triangle[(j + 1) % 3]
                z1, z2 = p1[2], p2[2]

                if (z1 - z) * (z2 - z) < 0:
                    t = (z - z1) / (z2 - z1)
                    intersection = p1 + t * (p2 - p1)
                    intersections.append(intersection[:2])  # (x, y)

            if len(intersections) == 2:
                segments.append((intersections[0], intersections[1]))

        all_segments.append(segments)

    return all_segments
