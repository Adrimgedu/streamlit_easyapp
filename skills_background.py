import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry  
from fun import write_data, read_data, get_country_code  # Ensure these functions handle Google Sheets
import cons as c  # Ensure this contains country list, area list, etc.
import altair as alt
import numpy as np



# Access the DataFrame from session state
if "df" in st.session_state:
    df = st.session_state["df"]
else:
    st.error("Data not found. Please navigate to the overview page first.")

skills = df[['skill_prog', 'skill_sql', 'skill_vis', 'skill_comp', 'skill_mat']].median()

# Plot the mean skill proficiency with labels inside the bars
fig2 = px.bar(y=skills.index,
              x=skills.values, labels={'x': 'Skills', 'y': 'Proficiency'},
              title='Mediana de Skills',
              orientation='h',
              text=skills.values)
fig2.update_xaxes(range=[0, 10])
fig2.update_traces(texttemplate='%{text:.2f}', textposition='inside')

#heatmap correlation of skills 
corr = df[['skill_prog', 'skill_sql', 'skill_vis', 'skill_comp', 'skill_mat']].corr()
fig3 = px.imshow(corr, text_auto=True, aspect="auto", title='Mapa de correlaciones Skills',
                 color_continuous_scale=px.colors.sequential.Burg)


# Pie chart for 'motivation'
motivation_counts = df['motivation'].value_counts()
fig4 = px.pie(values=motivation_counts.values, names=motivation_counts.index,
                title='Motivación', hole=0.3)
fig4.update_traces(textinfo='percent+label')

# Pie chart for 'ocupacion'
ocupacion_counts = df['ocupacion'].value_counts()
fig5 = px.pie(values=ocupacion_counts.values, names=ocupacion_counts.index,
                title='Ocupación actual', hole=0.3)
fig5.update_traces(textinfo='percent+label')


# Bar chart for 'bachelour' counts
bachelour_counts = df['bachelor'].value_counts()
fig6 = px.bar(y=bachelour_counts.index, x=bachelour_counts.values,
              title='Formación', orientation='h')
fig6.update_traces(texttemplate='%{y} / %{x}', textposition='inside')
fig6.update_yaxes(visible=False)


st.markdown('## Skills and Background')

# Display the bar chart in Streamlit
st.plotly_chart(fig6, theme="streamlit")

# Display the pie charts in Streamlit in a row with two columns
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig4, theme="streamlit")
with col2:
    st.plotly_chart(fig5, theme="streamlit")


    
# Display the plot in Streamlit
st.plotly_chart(fig2,theme="streamlit")
# Display the heatmap in Streamlit
st.plotly_chart(fig3,theme="streamlit")

