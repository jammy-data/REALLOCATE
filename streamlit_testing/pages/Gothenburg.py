import streamlit as st
import pandas as pd

st.logo("images/reallocate_logo.png", size = 'large')

if st.button("Homepage"):
    st.switch_page("Home.py")

st.title("Gothenburg Dataset Explorer")
st.write("This is a test page for the Gothenburg dataset explorer.")
st.write("You can add more functionality here as needed.")
st.write("This page is currently under construction.")

st.write("Similar format to the first page, but with different datasets.")
# Example of a button to switch to another page
if st.button("Go to Page 1"):
    st.switch_page("pages/page_1.py")

    st.write("---")

# --- Define paths and links for both images ---
# Image 1
image_path_1 = "https://reallocatemobility.eu/maintemplate/data/logos/logo.png"
link_url_1 = "https://reallocatemobility.eu"
alt_text_1 = "Reallocate Logo - Click to go to Google"

# Image 2
# Assuming you have another image, e.g., 'images/partner_logo.png'
# If not, you can use a placeholder for testing like:
# "https://via.placeholder.com/150x80/00FF00/000000?text=Partner+Logo"
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