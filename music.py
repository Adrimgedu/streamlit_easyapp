import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry  
from fun import write_data, read_data, get_country_code  # Ensure these functions handle Google Sheets
import cons as c  # Ensure this contains country list, area list, etc.
import altair as alt
import numpy as np
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
#from wordcloud import WordCloud

 
# Access the DataFrame from session state
if "df" in st.session_state:
    df = st.session_state["df"]
else:
    st.error("Data not found. Please navigate to the overview page first.")




#Cliente de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.getenv("SPOTIFY_TOKEN_ID"),
                                                           client_secret=os.getenv("SPOTIFY_TOKEN_SECRET")))


songs = df[['nombre_hash', 'song']].copy() #create a copy to avoid slice issues
songs.set_index('nombre_hash', inplace=True)

# Create new columns to store the Spotify data
songs['song_found'] = None
songs['song_release'] = None
songs['popularity'] = None
songs['genres'] = None
songs['artist_id'] = None
 
try:
    for nombre_hash, song in songs['song'].items(): #iterate through the series index and value
        result_song = sp.search(q=song, type='track', limit=1)
        if result_song['tracks']['items']:
                track = result_song['tracks']['items'][0]

                release_date = track['album']['release_date']
                popularity = track['popularity']
                artist_id = track['artists'][0]['id']
                artist_name = track['artists'][0]['name']

                artist_result = sp.artist(artist_id)
                
                genres = artist_result['genres'] if artist_result else []

                songs.loc[nombre_hash, 'song_found'] = track['name']
                songs.loc[nombre_hash, 'song_release'] = release_date
                songs.loc[nombre_hash, 'popularity'] = popularity
                songs.loc[nombre_hash, 'genres'] = ", ".join(genres)
                songs.loc[nombre_hash, 'artist_id'] = artist_name   
                
        else:
                print(f"Track '{song}' not found.")
                songs.loc[nombre_hash, 'song_found'] = "Not found"
except Exception as e:
        print(f"Error processing song '{song}': {e}")
finally:
    print("songs:",songs)
    write_data(songs.reset_index().values.tolist(), "ebis_ds_25_spotify") 

st.markdown('## What\'s your jam?')

st.write("### 🎵 Songs")
st.write("Estas son las canciones que hemos compartido")

#songs = read_data("ebis_ds_25_spotify")
#st.dataframe(songs)

# Calculate the mean popularity
mean_popularity = songs['popularity'].mean()

# Determine the color and text based on the mean popularity
if mean_popularity > 50:
    color = 'yellow'
    text = 'Somos un poco main stream'
else:
    color = 'pink'
    text = 'Somos un poco alternativos'


# Count how many song_releases are before 2018
release_dates_before_2018 = songs[songs['song_release'] < '2010-01-01'].shape[0]
#st.write(f"Number of songs released before 2018: {release_dates_before_2018}")
total = songs.shape[0]

if release_dates_before_2018 < total/2:
    text2 = "Somos un poco old school"
    color2 = "yellow"
else:
    text2 = "Somos un poco modernillos"
    color2 = "pink"
    


# Display the pie charts in Streamlit in a row with two columns
col1, col2 = st.columns(2)
with col1:
       
    fig = px.pie(values=[mean_popularity, 100 - mean_popularity], hole=0.7)
    fig.update_traces(marker=dict(colors=[color, 'white']), textinfo='none')

    # Add the text in the center of the donut chart
    fig.add_annotation(
        text=f"Popularidad: {round(mean_popularity,2)}",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=20, color='white'),
        xanchor='center', yanchor='middle'
    )

    # Display the text based on the mean popularity
    st.markdown(f"<h3 style='text-align: center;'>{text}</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig)

with col2:
    fig2 = px.pie(values=[total, total - release_dates_before_2018], hole=0.7)
    fig2.update_traces(marker=dict(colors=[color2, 'white']), textinfo='none')

    # Add the text in the center of the donut chart
    fig2.add_annotation(
        text=f"Canciones antes de 2010: {release_dates_before_2018}",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=20, color='white'),
        xanchor='center', yanchor='middle'
    )
    st.markdown(f"<h3 style='text-align: center;'>{text2}</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig2)




from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Combine all genres into a single string
text = ' '.join(songs['genres'].dropna().tolist())

# Create and generate a word cloud image:
wordcloud = WordCloud(collocations=False).generate(text)


st.markdown("<h3 style='text-align: center;'>🌌 El rollo de esta clase</h3>", unsafe_allow_html=True)
# Display the generated image:
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)