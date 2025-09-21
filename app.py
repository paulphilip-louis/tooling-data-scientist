import streamlit as st
import pandas as pd
import numpy as np

st.header("Visualizing meteorological data in Paris (1991-2024)")

@st.cache_data
def load_data():
    weather = pd.read_csv("data/weather.csv")
    return weather

data_load_state = st.tet("Loading data...")
weather = load_data()
data_load_state.text("Loading data... Done !")

