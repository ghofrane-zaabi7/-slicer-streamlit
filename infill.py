# infill.py

import numpy as np
from typing import List, Tuple
from numpy import ndarray

def generate_infill_segments(
    layer_segments: List[Tuple[ndarray, ndarray]],
    spacing: float = 10.0
) -> List[Tuple[ndarray, ndarray]]:
    """
    Génère un remplissage diagonal (45°) simple dans la bounding box des segments.
    Adapté à une imprimante à granulés (espacé, léger).
    """
    if not layer_segments:
        return []

    # Calculer les bornes XY du modèle à cette couche
    all_points = np.vstack([np.vstack([p1, p2]) for p1, p2 in layer_segments])
    min_x, min_y = np.min(all_points, axis=0)
    max_x, max_y = np.max(all_points, axis=0)

    infill_segments: List[Tuple[ndarray, ndarray]] = []
    diag_span = float(max_x - min_x + max_y - min_y)
    num_lines = int(diag_span / spacing)

    # Générer les lignes diagonales à 45°
    for i in range(-num_lines, num_lines + 1):
        offset = i * spacing

        p1 = np.array([min_x + offset, min_y])
        p2 = np.array([min_x, min_y + offset])

        # Clipper à la bounding box
        if float(p1[0]) > float(max_x) or float(p2[1]) > float(max_y):
            continue

        x1 = max(float(min_x), float(p1[0]))
        y1 = float(min_y) + (x1 - float(p1[0]))

        x2 = float(min_x)
        y2 = max(float(min_y), float(p2[1]))

        infill_segments.append((np.array([x1, y1]), np.array([x2, y2])))

    return infill_segments
