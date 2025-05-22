import streamlit as st
import pandas as pd

if st.button("Homepage"):
    st.switch_page("Home.py")

if st.button("Barcelona"):
    st.switch_page("pages/page_1.py")

st.title("Gothenburg Dataset Explorer")
st.write("This is a test page for the Gothenburg dataset explorer.")
st.write("You can add more functionality here as needed.")
st.write("This page is currently under construction.")

st.write("Similar format to the first page, but with different datasets.")
# Example of a button to switch to another page
if st.button("Go to Page 1"):
    st.switch_page("pages/page_1.py")