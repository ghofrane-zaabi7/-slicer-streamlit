def generate_gcode(layers, layer_height, extrusion_per_mm, output_file="output.gcode", add_brim=False,
                   nozzle_temp=200, bed_temp=60, print_speed=1500, travel_speed=3000):
    """
    Génère un fichier G-code à partir d'une liste de couches contenant des segments (paires de points).
    """
    gcode = []

    # En-tête de démarrage
    gcode.append("; --- G-code généré automatiquement ---")
    gcode.append("G21 ; Unités en mm")
    gcode.append("G90 ; Positionnement absolu")
    gcode.append("M82 ; Mode d'extrusion absolu")
    gcode.append(f"M104 S{nozzle_temp} ; Température buse")
    gcode.append(f"M140 S{bed_temp} ; Température plateau")
    gcode.append("G28 ; Auto-home")
    gcode.append(f"M109 S{nozzle_temp} ; Attente température buse")
    gcode.append(f"M190 S{bed_temp} ; Attente température plateau")
    gcode.append("G1 Z0.2 F1200 ; montée avant impression")
    gcode.append("G92 E0 ; reset extrusion")

    current_z = 0.2
    e_value = 0.0
    gcode.append("; --- Début de l'impression ---")

    for layer_idx, segments in enumerate(layers):
        current_z = 0.2 + layer_idx * layer_height
        gcode.append(f"; Layer {layer_idx + 1} Z={current_z:.2f}")

        for (x1, y1), (x2, y2) in segments:
            dx = x2 - x1
            dy = y2 - y1
            distance = (dx ** 2 + dy ** 2) ** 0.5
            extrusion = distance * extrusion_per_mm
            e_value += extrusion
            gcode.append(f"G1 X{x1:.2f} Y{y1:.2f} Z{current_z:.2f} F{travel_speed}")
            gcode.append(f"G1 X{x2:.2f} Y{y2:.2f} E{e_value:.5f} F{print_speed}")

    # Fin d'impression
    gcode.append("; --- Fin impression ---")
    gcode.append("M104 S0 ; Éteindre la buse")
    gcode.append("M140 S0 ; Éteindre le plateau")
    gcode.append("G1 X0 Y200 F3000 ; Recul de la tête")
    gcode.append("M84 ; Désactivation des moteurs")

    with open(output_file, "w") as f:
        f.write("\n".join(gcode))
