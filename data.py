import streamlit as st
import pandas as pd
st.title("競馬")
horse_all=pd.read_csv("Horse_Race.csv")
horse_all=horse_all.fillna(0)
horse_all["rank*class"]=horse_all["P_rank"]*horse_all["P_class-Class"]
horse_all["pop*class"]=horse_all["P_popular"]*horse_all["P_class-Class"]
st.write(horse_all)
