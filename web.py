import streamlit as st
import pandas as pd

st.title("My DA/ML web app")
st.success("Data sETS")

df = pd.read_csv("class.CSV")
st.dataframe(df)

