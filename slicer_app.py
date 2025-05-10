import streamlit as st
import os
import json
from config import settings
from stl_loader import load_stl
from slicer_core import slice_model
from infill import generate_infill_segments
from gcode_writer import generate_gcode

# Configuration de la page
st.set_page_config(page_title="Slicer 3D", layout="wide")

# 📌 Logo centré + titre avec colonnes
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo_greige.png", width=500)
    st.markdown("<h1 style='text-align: center;'>🖨️ Mon Slicer 3D – version web</h1>", unsafe_allow_html=True)

# 📁 Fonctions utilitaires profils
def list_profiles(folder="profiles"):
    profiles = []
    paths = []
    for file in os.listdir(folder):
        if file.endswith(".json"):
            profiles.append(file)
            paths.append(os.path.join(folder, file))
    return profiles, paths

def load_profile(path):
    with open(path, "r") as f:
        return json.load(f)

# 📂 Barre latérale complète
st.sidebar.header("📂 Paramètres d'entrée")

uploaded_file = st.sidebar.file_uploader("Fichier STL", type=["stl"])
profil_names, profil_paths = list_profiles()
selected_profile = st.sidebar.selectbox("Profil imprimante :", profil_names)
profile_path = profil_paths[profil_names.index(selected_profile)]
profile_data = load_profile(profile_path)

custom_profile = st.sidebar.file_uploader("📁 Charger un profil .json", type=["json"])
if custom_profile:
    profile_data = json.load(custom_profile)
    st.sidebar.success("✅ Profil personnalisé chargé avec succès !")

# 🧮 Réglages dynamiques dans la sidebar
layer_height = st.sidebar.number_input("Hauteur de couche (mm)", value=profile_data.get("layer_height", 0.2))
infill_spacing = st.sidebar.number_input("Espacement infill (mm)", value=profile_data.get("infill_spacing", 10.0))
nozzle_temp = st.sidebar.number_input("Température buse (°C)", value=profile_data.get("nozzle_temperature", 200))
bed_temp = st.sidebar.number_input("Température plateau (°C)", value=profile_data.get("bed_temperature", 60))
print_speed = st.sidebar.number_input("Vitesse impression (mm/min)", value=profile_data.get("print_speed", 1500))
travel_speed = st.sidebar.number_input("Vitesse déplacement (mm/min)", value=profile_data.get("travel_speed", 2000))
brim = st.sidebar.checkbox("Ajouter un brim", value=profile_data.get("add_brim", True))
gcode_filename = st.sidebar.text_input("Nom du fichier G-code", value="output.gcode")

# ▶️ Bouton de génération
if uploaded_file and st.sidebar.button("🚀 Lancer le slicing"):
    st.info(f"📥 Fichier STL : {uploaded_file.name}")
    st.info("📐 Tranchage en cours...")

    os.makedirs("temp", exist_ok=True)
    stl_path = os.path.join("temp", uploaded_file.name)
    with open(stl_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    mesh = load_stl(stl_path)
    layers = slice_model(mesh, layer_height)

    for i in range(len(layers)):
        infill = generate_infill_segments(layers[i], spacing=infill_spacing)
        layers[i].extend(infill)

    generate_gcode(
        layers,
        layer_height=layer_height,
        extrusion_per_mm=settings["extrusion_per_mm"],
        output_file=gcode_filename,
        add_brim=brim,
        nozzle_temp=nozzle_temp,
        bed_temp=bed_temp,
        print_speed=print_speed,
        travel_speed=travel_speed
    )

    st.success(f"✅ G-code généré : {gcode_filename}")

    # 📥 Télécharger le fichier G-code
    with open(gcode_filename, "rb") as file:
        st.download_button(
            label="📥 Télécharger le G-code",
            data=file,
            file_name=gcode_filename,
            mime="text/plain"
        )
