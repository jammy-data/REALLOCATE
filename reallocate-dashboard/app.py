import streamlit as st
import time
import json
import folium
from streamlit_folium import st_folium
from datetime import datetime
# from visualization_utils import create_barplot, create_linechart
from branca.element import Template, MacroElement
from helper_functions import value_to_color, average_color, get_binary_file, load_html, get_base64_image, filter_pilots_by_category
import streamlit.components.v1 as components
import random
import requests
import base64
import os
import pandas as pd
import re

# Load the legend template as an HTML element
legend_template = load_html("./static/legend_macro.html")
def get_api_url():
    # Check if we're inside Docker (by checking the environment variable)
    if os.getenv('DOCKER', 'false') == 'true':
        return "http://host.docker.internal:8000/pilot_api_data"
    else:
        return "http://127.0.0.1:8000/pilot_api_data"

st.set_page_config(page_title="My App", layout="wide")  # Adjust layout to wide for more space


pilots_static_df = pd.read_excel('./static/pilot_static_data.xlsx', engine="openpyxl")
print(pilots_static_df.head())

# Load JSON data
with open("./static/indicators.json") as f_ind:
    indicators = json.load(f_ind)

indicator_list = [item for sublist in indicators.values() for item in sublist]

with open("./pilot_sites.json") as f:
    pilots = json.load(f)

# Some session state initializations
if "kpi" not in st.session_state:
    st.session_state.kpi = indicator_list[0]
    st.session_state.legend = st.session_state.kpi
if "selected_sumi" not in st.session_state:
    st.session_state["selected_sumi"] = None
if "impact_area" not in st.session_state:
    st.session_state["impact_area"] = None
if "filtered_pilots_df" not in st.session_state:
    st.session_state["filtered_pilots_df"] = pilots_static_df

# Define a callback function to reset `selected_sumi`
def reset_sumi():
    st.session_state.legend = st.session_state.kpi
    if st.session_state["selected_sumi"] is not None:
        st.session_state["selected_sumi"] = None

# Define a callback function to reset `impact_area`
def reset_impact_area():
    if st.session_state["impact_area"] is not None:
        st.session_state["impact_area"] = None

logo1_base64 = get_base64_image("./static/logo.jpg")
logo2_base64 = get_base64_image("./static/REALLOCATE_Logo.png")


# Reapply filtering every time impact area or SUMI changes
def update_pilots():
    if "impact_area" in st.session_state or "selected_sumi" in st.session_state:
        if st.session_state.get("impact_area") is not None:
            st.session_state["filtered_pilots_df"] = filter_pilots_by_category(
                pilots_static_df, st.session_state["impact_area"]
            )
        elif st.session_state.get("selected_sumi") is not None:
            st.session_state["filtered_pilots_df"] = filter_pilots_by_category(
                pilots_static_df, st.session_state["selected_sumi"]
            )
        else:
            st.session_state["filtered_pilots_df"] = pilots_static_df  # Default: all pilots

# Executes when impact area button is clicked
def update_impact_area(area):
        st.session_state["impact_area"] = area
        reset_sumi()
        update_pilots()
        
# Removes all pilot realted filters
def reset_filters():
    st.session_state["selected_sumi"] = None
    st.session_state["impact_area"] = None
    st.session_state["filtered_pilots_df"] = pilots_static_df  # Reset to all pilots
    st.session_state.legend = st.session_state['kpi']

# Title of the app
st.markdown(
    f"""
    <div class="custom-container">
        <!-- Title on the left side -->
        <div class="header-container">
            <h1 class="custom-title1">Common Indicators</h1>
            <h2 class=custom-title2>{st.session_state.legend.replace("_", " ").title()}</h2>
        </div>
        <div class="logos-container">
            <img src="data:image/png;base64,{logo2_base64}" class="logo" alt="REALLOCATE logo" />
            <img src="data:image/jpeg;base64,{logo1_base64}" class="logo" alt="ITI logo" />
        </div>
        </div>
    </div>
    """, unsafe_allow_html=True
)
# st.markdown(f'<h1 class="custom-title">Common Indicators: {st.session_state.legend.replace("_", " ").title()}</h1>', unsafe_allow_html=True)
# st.title(f"Common Indicators: {st.session_state.legend.replace('_', ' ').title()}")       

# Initialize a 2-column layout (left for controls, right for the map)
col1, col2 = st.columns([1, 3])  # Adjust the ratio as needed

# Left column (col1): Controls
with col1:
    # Update the selected KPI
    # st.write("Choose a KPI:")
    
    
    selected_kpi = st.selectbox("Choose a KPI or click a UMI:", indicator_list, key='kpi', on_change=reset_sumi)
    st.write("\n")
    
    # st.header("SUMI categories")
    # st.write("Or choose a SUMI:")
    def update_sumi(sumi):
        st.session_state['impact_area'] = None
        st.session_state["selected_sumi"] = sumi
        st.session_state.legend = sumi
        update_pilots()
        # reset_impact_area()

    sumis = list(indicators.keys())
    for sumi in sumis:
        sumi_string = sumi.replace("_", " ").title()
        st.button(sumi_string, on_click=update_sumi, args=(sumi,))


    
# Function to encode local images as base64 and detect MIME type
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    
    # Detect MIME type based on file extension
    ext = os.path.splitext(image_path)[1].lower()
    mime_type = "image/svg+xml" if ext == ".svg" else "image/png"
    
    return f"data:{mime_type};base64,{encoded}"



# Load local images and convert to base64
image_paths = ["./static/road_safety.png", "./static/environment.png", "./static/governance.png", "./static/accessibility.png"]
image_base64 = [get_base64_image(img) for img in image_paths]

def render_buttons():
    empty_col1, col1, col2, col3, col4, empty_col2 = st.columns([1, 2, 2, 2, 2, 1])
    impact_areas = ["Road Safety", "Environmental", "Transformative Governance", "Inclusivity/Accessibility"]
    # col1, col2, col3, col4 = st.columns(4)
    
    for idx, col in enumerate([col1, col2, col3, col4]):
        with col:
            button_html = f"""
            <div class="image-button">
                <img src="{image_base64[idx]}" alt="Button {idx + 1}">
            </div>
            """
            st.markdown(button_html, unsafe_allow_html=True)
            # st.button(f"{impact_areas[idx]}", on_click=update_impact_area, args=(impact_areas[idx],))
            if st.button(f"{impact_areas[idx]}", key=f"{impact_areas[idx]}", type="primary"):
                update_impact_area(f"{impact_areas[idx]}")


render_buttons()



# Right column (col2): Map
with col2:
    # Initialize the map with a default center (centered on Europe)
    m = folium.Map(location=[50, 10], zoom_start=4)

    macro = MacroElement()
    macro._template = Template(legend_template)
    m.get_root().add_child(macro)

    for index, row in st.session_state['filtered_pilots_df'].iterrows():
        lat = row['lat']
        lon = row['lon']
        site_name = row['name']
        site_lower = row['name'].lower()  # Convert site to lowercase

        with open(f"./lyon_indicators_dummy.json") as f1: # open same dummy data for all pilots
            indicator_data = json.load(f1)

        # Check the selected SUMI or KPI and set color
        if st.session_state.selected_sumi is not None:
            sumi_indicators = indicators[st.session_state.selected_sumi]
            color_list = []
            # Calculate UMI color as average of its indicator colors
            for indicator in sumi_indicators:
                if indicator.lower().replace(" ", "_") in indicator_data.keys():
                    indicator_values = indicator_data[indicator.lower().replace(" ", "_")]
                    color = value_to_color(indicator_values)
                else:
                    color = f"rgb(128, 128, 128)"  # grey
                color_list.append(color)
            current_color = average_color(color_list)
            map_file = "{}_map.html".format(st.session_state.selected_sumi)
        elif st.session_state.kpi.lower().replace(" ", "_") in indicator_data.keys():
            indicator_values = indicator_data[st.session_state.kpi.lower().replace(" ", "_")]
            current_color = value_to_color(indicator_values)
            map_file = "{}_map.html".format(st.session_state.kpi.lower().replace(" ", "_"))
        else:
            current_color = f"rgb(128, 128, 128)"  # grey
            map_file = "{}_map.html".format(st.session_state.kpi.lower().replace(" ", "_"))


        try:
            api_url = get_api_url()
            response = requests.get(api_url, params={"site_name": site_name})
            # response = requests.get("http://127.0.0.1:8000/pilot_api_data", params={"site_name": site_name})
            response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
            data = response.json()

        
            # Extract weather, AQI, and traffic data
            temperature = data[site_name]['weather'].get("temperature", "N/A")
            humidity = data[site_name]['weather'].get("humidity", "N/A")
            precipitation = data[site_name]['weather'].get("precipitation", "N/A")
            aqi = data[site_name]['air_quality'].get("AQI", "N/A")  # Default to max AQI if missing
            traffic = data[site_name]['traffic'].get("congestion_level", "N/A")

            # Build popup content dynamically
            popup_string = f"""
            <b>{site_name}</b><br>
            🌡️&nbsp;{temperature}°C&nbsp;&nbsp;
            💧&nbsp;{humidity}%&nbsp;&nbsp;
            ☔&nbsp;{precipitation}mm&nbsp;&nbsp;
            🍃&nbsp;{round(((500 - aqi) / 500) * 100)}%&nbsp;&nbsp;
            🚗&nbsp;{round(traffic * 100)}%&nbsp;
            """
        except requests.exceptions.RequestException as e:
            popup_string = f"<b>{site_name}</b><br>Error fetching data: {e}"

        # Add circle marker for each site
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            popup=popup_string,
            color=current_color,
            fill=True,
            fill_color=current_color,
            fill_opacity=0.6
        ).add_to(m)
     

    # Save the map to an HTML file
    m.save(map_file)

    # Encode to base64
    map_data = get_binary_file(map_file)
    b64_map = base64.b64encode(map_data).decode()
    
    # Create a download button
    with col1:
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.download_button(
            label="📥 Download Map",
            data=map_data,
            file_name=map_file,
            mime="text/html"
        )
        st.button("🔄 Remove Filters", key="reset-button", type="secondary", on_click=reset_filters)
        
            
    st_folium(m, width='100%', height=600, key="map_initial_load")


st.markdown(
    f"""
    <div class="custom-container">
        <!-- Title on the left side -->
        <div class="header-container">
            <h1 class=custom-title1>Pilots</h1>
        </div>
    </div>
    <br>
    """, unsafe_allow_html=True
)

for index, row in st.session_state['filtered_pilots_df'].iterrows():

    intervention_start = row['Start Date']
    intervention_end = row['End Date']
    start_date = pd.to_datetime(intervention_start)
    end_date = pd.to_datetime(intervention_end)

    # Display row with an expand feature
    with st.expander(f" {row['name']}"):
        
        st.write(f"📍 **City:** {re.sub(r'\(.*?\)', '', row['name']).strip()}")
        st.write(f"📅 **Start Date:** {start_date}")
        st.write(f"📅 **End Date:** {end_date}")
        
        # Display additional info (description, lessons learned, image)
        st.write(f"📝 **Description:** {row['Description']}")
        st.write(f"💡 **Lessons Learned:** {row['Lessons Learned']}")
        

        # Display image from URL
        # st.image(row['Pictures'], caption=f"Image of {row['name']}", width=300)
        st.markdown(f'<img src="{row["Pictures"]}" alt="Image of {row['name']}" width="300" class="city-image" />', unsafe_allow_html=True)


        # Optional: Button to navigate/select
        if st.button(f"Show more", key=row['name']):
            st.write(f"You selected {row['name']}!")


# Button click logic (simulated, replace with URL parameter handling)
# site_clicked = st.query_params.get("site")
# if site_clicked:
    # TODO: This action should open a new interface displaying KPI graphs
    # st.write(f"You clicked on {site_clicked}")

st.markdown(
    f"""
    <div class="footer-container">
        <div class="footer-text">
            © 2025 CERTH-ITI. All rights reserved.
        </div>
        <div class="footer-logos">
            <img src="data:image/jpeg;base64,{logo1_base64}" class="footer-logo" alt="ITI logo" />
            <img src="data:image/png;base64,{logo2_base64}" class="footer-logo" alt="REALLOCATE logo" />
        </div>
    </div>
    """,
    unsafe_allow_html=True
)





# Custom CSS styles
with open("./static/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


components.html(f"""
    <script>
        function sendMessage(sumi) {{
            const streamlitInput = window.parent.document.querySelector("input[pilots-testid='stTextInput']");
            streamlitInput.value = sumi;
            streamlitInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
    </script>
""", height=200)




# Render KPIs only if there is a selection
# if st.session_state.city:  # Check if there is a valid KPI selection
#     st.session_state.selected_kpi = selected_kpi
#     render_kpis(st.session_state.selected_kpi)  # Render only selected KPIs
                                    


# TO DO LIST                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
# TODO: Log in and roles? (needs to be discussed though)
# TODO: When indicators are finalized replace their matching with UMIs in the indicators.json file, currently a dummy matching is implemented
# TODO: Replace with actual pictures and coordinates for pilots

