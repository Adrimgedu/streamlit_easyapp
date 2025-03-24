import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry  
from fun import write_data, read_data, get_country_code  
import cons as c   
import altair as alt
import numpy as np
import os

print("🔍 Cargando datos...")


if "df" not in st.session_state:
    df = read_data(os.getenv("SHEET_NAME"))
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

st.markdown('#### Estadísticas rápidas')
row1 = st.columns(3)    

with row1[0]:
    st.metric(label=" 👨 Respuestas", value=df.shape[0])
with row1[1]:
    st.metric(label="⌛ Media edad", value=round(np.mean(df['edad']),2))

with row1[2]:
    st.metric(label="🗺️ Países", value=df['pais'].nunique(),help="Cantidad de países representados")

    


st.markdown('#### Datos Principales')

st.write("### 📋 Datos Ingresados:")
st.dataframe(df.drop(columns=["nombre"], errors="ignore").rename(columns={"nombre_hash": "Id anonimo"}))

# --- Age Distribution ---
st.write("### 📊 Distribución de Edades")
fig1 = px.histogram(df, x="edad", title="Distribución de Edades", nbins=20)
fig1.update_xaxes(range=[17, 80])
st.plotly_chart(fig1)

# --- Choropleth Map ---
st.write("### 🌎 Mapa de Nacionalidades")

if not df.empty:
    df["ISO_A3"] = df["pais"].apply(get_country_code)
    df = df.dropna(subset=["ISO_A3"])

    country_counts = df["ISO_A3"].value_counts().reset_index()
    country_counts.columns = ["ISO_A3", "count"]

    fig3 = px.choropleth(
        country_counts, 
        locations="ISO_A3", 
        color="count", 
        hover_name="ISO_A3", 
        color_continuous_scale=px.colors.sequential.Burg, 
        title="Distribución Global",
        range_color=(1, country_counts["count"].max())
    )
    st.plotly_chart(fig3)
else:
    st.warning("No hay suficientes datos para generar el mapa.")
