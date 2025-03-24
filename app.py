import streamlit as st
import pandas as pd
import os
import plotly.express as px
import pycountry  
from fun import * 
import cons as c  
from st_social_media_links import SocialMediaIcons

st.logo("img/logo_adri.png")

# Page configuration
st.set_page_config(
    page_title="📊 Kickoff EBIS Data Science",
    menu_items={ "About": "mailto:adrian.munnoz.garcia@gmail.com"},
    layout="centered",
    initial_sidebar_state="expanded")


alt.theme.enable("vox")

print("🚀 Iniciando la aplicación...")
print("🔍 Cargando datos...")

###### Page Layout ######

# --- Sidebar ---
st.sidebar.title("📊 Kickoff EBIS Data Science")
st.sidebar.markdown("¡Bienvenido! Completa el formulario para conocer mejor quienes somos en el master de Data Science. **Recuerda que los datos son totalmente anónimos y solo serán utilizados para motivos interactivos de la sesión**")


st.sidebar.markdown("Yo soy Adrián Muñoz, Senior Data Scientist en Indra. Me encanta la docencia y la divulgación de la ciencia de datos. ¡Encantado de conocerte! Estaré encantando de acompañarte en este master.")

 
with st.sidebar:
    st.image("img/logo_adri.png", caption="Adrián Muñoz")

    social_media_links = [
        "https://www.linkedin.com/in/adrian-munoz-garcia/",
        "https://github.com/Adrimgedu",
    ]

    social_media_icons = SocialMediaIcons(social_media_links)

    social_media_icons.render()

# Initialize session state
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=[
        "Nombre",
        "Nombre Hash",
        "Edad",
        "Carrera Universitaria",
        "Ocupación",
        "Área de interés",
        "País",
        "Programación",
        "SQL",
        "Visualización de Datos",
        "Comprensión de Datos",
        "Matemáticas generales",
        "Motivación Principal",
        "Canción Favorita"
    ])
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False  # Track submission per user session

#st.title("📊 Kickoff EBIS Data Science")

# --- Formulario de ingreso ---
st.write("### 📝 ¿Quiénes somos?")
if not st.session_state["submitted"]:
    with st.form("formulario"):
        # Personal Info
        nombre = sanitize_input(st.text_input("Nombre"))
        edad = st.number_input("Edad", min_value=17, max_value=80,value=None)

        # Multi-level Dictionary Select (Bachelor)
        all_suboptions = sorted([sub for subs in c.carreras.values() for sub in subs])  
        bachelor = st.selectbox("Carrera Universitaria",index=None,options=all_suboptions,placeholder="Selecciona una carrera o formación que más se apróxime")  

        # Occupation
        ocupacion = st.selectbox("Ocupación", ['Trabajo', 'Estudiando', 'Ambas'],index=None,placeholder="En qué estás ocupado actualmente (Sin contar este Máster)")

        # Area & Country
        area = st.selectbox("Área de interés", c.areas,index=None,placeholder="Selecciona el campo de donde vienes")
        pais = st.selectbox("País", c.countries,index=None,placeholder="Desde donde te conectas")

        # --- Skill Group ---
        st.text("🛠️ Grupo de preguntas sobre tu valoración en habilidades relacionadas con DS")
        with st.expander("💻 Habilidades (0 - 10)"):
            skill_prog = st.slider("Programación", 0, 10, 5)
            skill_sql = st.slider("SQL", 0, 10, 5)
            skill_vis = st.slider("Visualización de Datos", 0, 10, 5)
            skill_comp = st.slider("Comprensión de Datos", 0, 10, 5)
            skill_mat = st.slider("Matemáticas generales", 0, 10, 5)

        # Motivation
        motivation = st.selectbox("Motivación Principal", c.motivaciones, index=None, placeholder="¿Qué te motiva a estudiar Data Science?")

        # Favorite Song
        song = sanitize_input(st.text_input("Canción Favorita", placeholder="¿Cuál es tu canción favorita actualmente?. Escribe la canción sin el artista Ej: Bohemian Rhapsody"))

        # Submit Button
        submit = st.form_submit_button("Enviar")

        if submit:
            errors = validate_form(nombre, edad, bachelor, ocupacion, area, pais, skill_prog, skill_sql, skill_vis, skill_comp, skill_mat, motivation, song)

            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Hash Name for Privacy
                nombre_hash = hash_con_valor(nombre, os.getenv('HASH_VALUE'))
                print(f"nombre_hash{nombre_hash}")
                # Read existing data to prevent duplicate submissions
                #df_existing = read_data()
                #if nombre_hash in df_existing["Nombre"].values:
                #    st.warning("⚠️ Ya has enviado datos. No se permiten múltiples envíos.")
                #    st.stop()

                # Append to Google Sheets
                write_data([nombre, nombre_hash, edad, bachelor, ocupacion, area, pais, skill_prog, skill_sql, skill_vis, skill_comp, skill_mat, motivation, song],
                           os.getenv('SHEET_NAME'))

                # Store submitted data in session state
                df = pd.DataFrame({
                    "Nombre": [nombre_hash],
                    "Edad": [edad],
                    "Carrera Universitaria": [bachelor],
                    "Ocupación": [ocupacion],
                    "Área de interés": [area],
                    "País": [pais],
                    "Programación": [skill_prog],
                    "SQL": [skill_sql],
                    "Visualización de Datos": [skill_vis],
                    "Comprensión de Datos": [skill_comp],
                    "Matemáticas generales": [skill_mat],
                    "Motivación Principal": [motivation],
                    "Canción Favorita": [song]
                })
                st.session_state["data"] = df
                st.session_state["submitted"] = True  
                st.toast("✅ Datos enviados exitosamente!")

# --- Show warning only after submission ---
if st.session_state["submitted"]:
    st.warning("✅ Ya has enviado tus datos en esta sesión")

# --- Display Submitted Data ---
st.write("### 📋 Datos Ingresados:")
st.dataframe(st.session_state['data'])
