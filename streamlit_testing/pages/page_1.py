"""Streamlit app to fetch and display datasets from a given API with caching and error handling."""

from io import StringIO, BytesIO
import streamlit as st 
import requests
import pandas as pd
import plotly.express as px


# Define your datasets and the shared API key
API_KEY = "e58ce2d31573401158da989c0906bb09"
API_URL = "https://portaldades.ajuntament.barcelona.cat/services/backend/rest/statistic/export"
#Add the datasets we need here
DATASETS = {
    "Walking journeys": API_URL + "?id=wc9hkmubl7&fileformat=CSV",
    "Bike & PMV by sex": API_URL + "?id=5cid3dkbbx&fileformat=CSV"
}
#Add a home button to go back to the homepage
if st.button("Homepage"):
    st.switch_page("Home.py")
#Add a button to go to the Gothenberg page
if st.button("Gothenberg"):
    st.switch_page("pages/page_2.py")
# Streamlit dropdown
st.title("Dataset Explorer")
dataset_name = st.selectbox("Choose a dataset", list(DATASETS.keys()))

# Fetch data
url = DATASETS[dataset_name]
headers = {"X-IBM-Client-Id": API_KEY}  # or use "?api_key=..." if it's query-based

@st.cache_data  # Cache results to avoid repeated API calls
#This function loads data from API and handles different content types
def load_data(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "").lower()

    if "application/json" in content_type:
        return pd.DataFrame(response.json())

    elif "text/csv" in content_type or "application/csv" in content_type:
        return pd.read_csv(StringIO(response.text))

    elif "application/octet-stream" in content_type:
        # Could be a downloadable CSV
        return pd.read_csv(BytesIO(response.content))

    else:
        raise ValueError(f"Unsupported content type: {content_type}")

try:
    df = load_data(url)
    df[df.columns[0]] = pd.to_datetime(df['Dim-00:TEMPS'], utc=True)
    st.write(f"Preview of **{dataset_name}**:")
    st.dataframe(df.head())
    # Exclude 'Dim-00:TEMPS' from VARIABLES
    VARIABLES = [col for col in df.columns if col != 'Dim-00:TEMPS']
    variable_name = st.selectbox("Choose a variable", VARIABLES)
    grouped = df.groupby(['Dim-00:TEMPS', variable_name]).sum()
    grouped['VALUE'].unstack(variable_name)
    grouped = grouped.reset_index()
    # Two columns
 #   col1, col2 = st.columns(2)
 #   with col1:
    # Simple Plotly graph - customize this based on actual data columns
    fig = px.line(grouped, x=grouped['Dim-00:TEMPS'], y=grouped['VALUE'], color= variable_name,title=f"{dataset_name} Overview")
    st.plotly_chart(fig)

except Exception as e:
    st.error(f"Failed to load data: {e}")
