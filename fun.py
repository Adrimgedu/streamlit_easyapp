import pycountry

def get_country_code(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except LookupError:
        return None



####################

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os 
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_google_sheet(sheet_name):
    """Authenticate and get the Google Sheet"""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('CREDENTIALS_FILE'), scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open(os.getenv('SPREADSHEET'))
    return spreadsheet.worksheet(sheet_name)

def read_data(sheet_name):
    """Read data from Google Sheets into a DataFrame"""
    sheet = get_google_sheet(sheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def write_data(new_data,sheet_name):
    """Append new data to Google Sheets"""
    sheet = get_google_sheet(sheet_name)
    for row in new_data:
        sheet.append_row(row)

######################################################

import hashlib

def hash_con_valor(cadena, valor):
    """
    Hashea una cadena combinándola con otro valor.

    Args:
        cadena (str): La cadena que se va a hashear.
        valor (str): El valor adicional que se combinará con la cadena.

    Returns:
        str: El hash resultante en formato hexadecimal.
    """

    # Combinamos la cadena y el valor
    cadena_combinada = cadena + str(valor)  # Convertimos el valor a cadena

    # Codificamos la cadena combinada a bytes
    cadena_codificada = cadena_combinada.encode('utf-8')

    # Creamos un objeto hash SHA-256
    hash_objeto = hashlib.sha256()

    # Actualizamos el objeto hash con la cadena codificada
    hash_objeto.update(cadena_codificada)

    # Obtenemos el hash en formato hexadecimal
    hash_hexadecimal = hash_objeto.hexdigest()

    return hash_hexadecimal

######################################################
import re
import cons as c

def sanitize_input(text):
    """Removes potentially harmful characters from user input"""
    return re.sub(r'[^\w\s]', '', text.strip())  # Remove special characters

def validate_form(nombre, edad, bachelor, ocupacion, area, pais, skill_prog, skill_sql, skill_vis, skill_comp, skill_mat, motivation, song):
    errors = []
    
    if not nombre or len(nombre) < 2:
        errors.append("⚠️ Nombre debe tener al menos 2 caracteres.")
    if edad < 17 or edad > 80:
        errors.append("⚠️ Edad debe estar entre 17 y 80 años.")
    if bachelor not in [sub for subs in c.carreras.values() for sub in subs]:
        errors.append("⚠️ Carrera universitaria no válida.")
    if ocupacion not in ['Trabajo', 'Estudiando', 'Ambas']:
        errors.append("⚠️ Ocupación no válida.")
    if area not in c.areas:
        errors.append("⚠️ Área de interés no válida.")
    if pais not in c.countries:
        errors.append("⚠️ País no válido.")
    if not (0 <= skill_prog <= 10 and 0 <= skill_sql <= 10 and 0 <= skill_vis <= 10 and 0 <= skill_comp <= 10 and 0 <= skill_mat <= 10):
        errors.append("⚠️ Las habilidades deben estar entre 0 y 10.")
    if motivation not in c.motivaciones:
        errors.append("⚠️ Motivación no válida.")
    if len(song) < 2:
        errors.append("⚠️ Canción favorita debe tener al menos 2 caracteres.")

    return errors

######################################################
import altair as alt

# Donut chart
def make_donut(input_response, input_text, input_color):
    chart_color = ['#F39C12', '#875A12']

    source = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100-input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100, 0]
    })
        
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
        
    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
    return plot_bg + plot + text

def display_spain_percentage():
    df = read_data()
    total_count = len(df)
    spain_count = len(df[df['pais'] == 'Spain'])
    spain_percentage = (spain_count / total_count) * 100 if total_count > 0 else 0
    return make_donut(spain_percentage, 'Spain', ['#F39C12', '#875A12'])