"""Streamlit app to fetch and display datasets from a given API with caching and error handling."""

from io import StringIO, BytesIO
import streamlit as st 
import requests
import pandas as pd
import plotly.express as px


# Define your datasets and the shared API key
API_KEY = "e58ce2d31573401158da989c0906bb09"
API_URL = "https://portaldades.ajuntament.barcelona.cat/services/backend/rest/statistic/export"
DATASETS = {
    "Walking journeys": API_URL + "?id=wc9hkmubl7&fileformat=CSV",
    "Bike & PMV by sex": API_URL + "?id=5cid3dkbbx&fileformat=CSV"
}

# Streamlit dropdown
st.title("Dataset Explorer")
dataset_name = st.selectbox("Choose a dataset", list(DATASETS.keys()))

# Fetch data
url = DATASETS[dataset_name]
headers = {"X-IBM-Client-Id": API_KEY}  # or use "?api_key=..." if it's query-based

@st.cache_data  # Cache results to avoid repeated API calls
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

    # Simple Plotly graph - customize this based on actual data columns
    fig = px.line(df, x=df.columns[0], y=df.columns[1], title=f"{dataset_name} Overview")
    st.plotly_chart(fig)

except Exception as e:
    st.error(f"Failed to load data: {e}")
