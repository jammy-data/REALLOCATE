import streamlit as st

PILOTS = ["Barcelona", "Gothenburg"]
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
)
with st.form("pilot_form"):
    pilot_name = st.selectbox("Choose a variable", PILOTS)
    submitted = st.form_submit_button("Go to pilot page")
    if submitted:
        st.switch_page(f"pages/{pilot_name}.py")


