import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry  
from fun import write_data, read_data, get_country_code  
import cons as c  
import altair as alt
import numpy as np


#######################
# Page configuration
st.set_page_config(
    page_title="📊 Kickoff EBIS Data Science VISUALIZATION",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.theme.enable("vox")
#######################
print("🚀 Iniciando la aplicación...")


pages = {
    "overview": [st.Page("overview.py", title="Vista rápida")],
    "skills_background": [st.Page("skills_background.py", title="Skills & Background")],
    "music": [st.Page("music.py", title="Cuál es el rollo?")]
}

# Set the default page to "overview"
pg = st.navigation(pages)
pg.run()
