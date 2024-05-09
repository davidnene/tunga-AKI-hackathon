import pandas as pd
import streamlit as st


@st.cache_data
def load_data(allow_output_mutation=True):
   return pd.read_csv("data.csv")


