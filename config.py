# config.py

settings = {
    # 📂 Fichier STL à charger
    "stl_file": "Chubby_Shark.stl",

    # 📐 Paramètres de tranchage
    "layer_height": 0.2,              # Hauteur de couche en mm
    "extrusion_per_mm": 0.05,         # Quantité d'extrusion par mm (à adapter)

    # 🔥 Températures
    "nozzle_temp": 200,               # Température de la buse (°C)
    "bed_temp": 60,                   # Température du plateau (°C)

    # 🚀 Vitesse (en mm/min — Marlin utilise cette unité)
    "print_speed": 1800,              # Vitesse d'impression (ex. 30 mm/s)
    "travel_speed": 3000,             # Vitesse de déplacement (ex. 50 mm/s)

    # 🧱 Remplissage
    "infill_spacing": 10.0,           # Espacement du remplissage (mm)

    # 💾 G-code export
    "output_gcode_file": "output.gcode"
}
