"""Streamlit app to fetch and display datasets from a given API with caching and error handling."""

from io import StringIO, BytesIO
import streamlit as st 
import requests
import pandas as pd
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point

st.logo("images/reallocate_logo.png", size = 'large')

# Define your datasets and the shared API key
API_KEY = "e58ce2d31573401158da989c0906bb09"
API_URL = "https://portaldades.ajuntament.barcelona.cat/services/backend/rest/statistic/export"
DATASET_URL = 'https://opendata-ajuntament.barcelona.cat/data/api/action/datastore_search'
#Add the datasets we need here
DATASETS = {
    "Walking journeys": API_URL + "?id=wc9hkmubl7&fileformat=CSV",
    "Bike & PMV by sex": API_URL + "?id=5cid3dkbbx&fileformat=CSV",
    "Public accessibility": DATASET_URL + "?resource_id=8c8cbb08-31e1-4c0b-92e5-c01e6598469c"
}
#Add a home button to go back to the homepage
if st.button("Homepage"):
    st.switch_page("Home.py")

# Streamlit dropdown
st.title("Dataset Explorer")
dataset_name = st.selectbox("Choose a dataset", list(DATASETS.keys()))

# Fetch data
url = DATASETS[dataset_name]
headers = {"X-IBM-Client-Id": API_KEY}  # or use "?api_key=..." if it's query-based
headers_gdf = {'Authorization': API_KEY}

@st.cache_data
def load_data(url):
    # Try standard tabular headers first
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "").lower()

    # Try to load as tabular data
    try:
        if "application/json" in content_type:
            df = pd.DataFrame(response.json())
        elif "text/csv" in content_type or "application/csv" in content_type:
            df = pd.read_csv(StringIO(response.text))
        elif "application/octet-stream" in content_type:
            df = pd.read_csv(BytesIO(response.content))
        else:
            raise ValueError("Unknown content type")

        # Quick heuristic: wrong header gives dummy column like "help"
        if df.columns[0].lower() == "help":
            raise ValueError("Got fallback/help response — retrying as GeoDataFrame")

        return df

    except Exception:
        # Retry using GeoDataFrame headers
        response = requests.get(url, headers=headers_gdf)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['result']['records'])
        return df


try:
    df = load_data(url)
    #df[df.columns[0]] = pd.to_datetime(df['Dim-00:TEMPS'], utc=True)
    st.write(f"Preview of **{dataset_name}**:")
    st.dataframe(df.head())
    # Exclude 'Dim-00:TEMPS' from VARIABLES
#    # We need to create a specific if function to handle geographic dataframes
    if 'Gis_X' in df.columns:
        # Create a GeoDataFrame from the DataFrame
        geometry = [Point(xy) for xy in zip(df['Longitud_X_WGS84'], df['Latitud_Y_WGS84'])]
        gdf = gpd.GeoDataFrame(df, geometry = geometry, crs="EPSG:4326")
        gdf["lati"] = gdf.geometry.y
        gdf["longi"] = gdf.geometry.x
        fig = px.scatter_map(
        gdf,
        lat=gdf['lati'],
        lon=gdf["longi"],
        color='Situació',
        zoom = 10,
        hover_data = {"Data d'Alta":True,
                   "Situació": True,
                   "lati": False,
                   "longi": False},
   )
        fig.update_layout(map_style="carto-darkmatter")
        st.plotly_chart(fig)
    else:
        VARIABLES = [col for col in df.columns if col != 'Dim-00:TEMPS']
        variable_name = st.selectbox("Choose a variable", VARIABLES)
        grouped = df.groupby(['Dim-00:TEMPS', variable_name]).sum()
        grouped['VALUE'].unstack(variable_name)
        grouped = grouped.reset_index()
    # Two columns
 #   col1, col2 = st.columns(2)
 #   with col1:
    # Simple Plotly graph
        fig = px.line(grouped, x=grouped['Dim-00:TEMPS'], y=grouped['VALUE'], color= variable_name,title=f"{dataset_name} Overview")
        st.plotly_chart(fig)

except Exception as e:
    st.error(f"Failed to load data: {e}")

##########################################################
st.write("---")

# --- Define paths and links for both images ---
# Image 1
image_path_1 = "https://reallocatemobility.eu/maintemplate/data/logos/logo.png"
link_url_1 = "https://reallocatemobility.eu"
alt_text_1 = "Reallocate Logo - Click to go to Google"

# Image 2
image_path_2 = "https://www.bsc.es/sites/default/files/public/styles/bscw2_-_simple_crop_style/public/bscw2/pages/discover-bsc/bsc-branding-identity-logo-header_0.jpg?itok=BdjkMwL6&sc=569a3a63c536723072a6d292da3890ca"
link_url_2 = "https://www.bsc.es" # Replace with your second link
alt_text_2 = "Partner Logo - Click to go to Example.com"

# --- Inject Custom CSS for Flexbox Layout ---
st.markdown(
    """
    <style>
    .image-container {
        display: flex; /* Makes the children (images) display in a row */
        justify-content: center; /* Centers the images horizontally */
        align-items: center; /* Vertically aligns images if they have different heights */
        gap: 20px; /* Adds space between the images */
        margin-top: 20px; /* Add some space above the container */
        margin-bottom: 20px; /* Add some space below the container */
    }

    .image-container img {
        height: auto; /* Maintain aspect ratio */
        max-height: 80px; /* Set a max height for both images */
        width: auto; /* Let width adjust based on height */
        max-width: 150px; /* Set a max width for both images */
        /* Add any other common styling here, e.g., border, border-radius */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Use Markdown to embed HTML with both linked images ---
st.markdown(
    f"""
    <div class="image-container">
        <a href="{link_url_1}" target="_blank">
            <img src="{image_path_1}" alt="{alt_text_1}">
        </a>
        <a href="{link_url_2}" target="_blank">
            <img src="{image_path_2}" alt="{alt_text_2}">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("---")