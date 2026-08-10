import streamlit as st
import pandas as pd
from predict import get_prob, get_global_mean_play_rate
from PIL import Image
import random
import os

gradient_style = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1f4068, #162447, #e43f5a);
    background-size: cover;
}
[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
}
</style>
"""

st.html(gradient_style)

st.header("WHAT WOULD THEY PLAY?")
st.subheader("Type in your favorite Dave Matthews Band song, get the probability of it playing at the next show!")
st.markdown("Data routinely sourced from DMBAlmanac.")
st.divider()

FOLDER_PATH_1 = "./happydave"

FOLDER_PATH_2 = "./saddave"

@st.cache_data
def get_image_list(folder):
    if not os.path.exists(folder):
        return []
    return [
        f for f in os.listdir(folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
    ]

@st.cache_data
def load_and_prep_data():
    df = pd.read_csv("necessary/.streamlit/allshows.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%m.%d.%Y").dt.date
    df["Song"] = df["Song"].str.lower()
    mean_rate = get_global_mean_play_rate(df)
    return df, mean_rate, df['Song'].unique()

data, global_mean_rate, valid_songs = load_and_prep_data()

song = st.text_input("Your favorite DMB song: ")

button_clicked = st.button("Give me the numbers!")

if "random_image" not in st.session_state:
    st.session_state.random_image = None
if "selected_folder" not in st.session_state:
    st.session_state.selected_folder = None

if button_clicked:
    clean_song = song.strip().lower()
    
    if clean_song not in valid_songs:
        st.error("Sorry, that song is not in the database. Try another song!")
    else:
        prob = get_prob(data, clean_song, global_mean_rate)
        
        prob_percent = f"{prob * 100:.2f}"

        if (prob * 100) < 20:
            current_folder = FOLDER_PATH_2
        else:
            current_folder = FOLDER_PATH_1

        images = get_image_list(current_folder) 

        if images:
            st.session_state.random_image = random.choice(images)
            st.session_state.selected_folder = current_folder
        else:
            st.session_state.random_image = None
            st.session_state.selected_folder = None
            st.warning("No images found in the folder.")
        
        st.success(f"The probability of hearing **{song}** at the next DMB show is **{prob_percent}%**!")
        st.markdown("Type in another song to get another probability!")

if st.session_state.random_image and st.session_state.selected_folder:
    full_path = os.path.join(
        st.session_state.selected_folder, st.session_state.random_image
    )
    opened_image = Image.open(full_path)
    st.image(opened_image, use_container_width=True)