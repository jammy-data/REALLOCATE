import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Homepage with test buttons")

if st.button("Go to Page 1"):
    st.switch_page("page_1.py")
