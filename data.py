import streamlit as st
import pandas as pd
horse_all=pd.read_csv("Horse_Race.csv")
st.write(horse_all)