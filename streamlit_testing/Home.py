import streamlit as st
import pandas as pd
import plotly.express as px

st.sidebar.success("Select a demo above.")
st.title("Homepage with test buttons")

if st.button("Barcelona"):
    st.switch_page("pages/page_1.py")
if st.button("Gothenburg"):
    st.switch_page("pages/page_2.py")

