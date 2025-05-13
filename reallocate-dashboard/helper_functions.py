import re
import json
import requests
import time
from datetime import datetime
import base64
from dotenv import load_dotenv
import os

MET_URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact"

load_dotenv()
WAQI_API_KEY = os.getenv("WAQI_API_KEY")
# print(WAQI_API_KEY)
TRAFFIC_API_KEY = os.getenv("TRAFFIC_API_KEY")
# print(TRAFFIC_API_KEY)

def fetch_weather(lat, lon):
    """ Fetch weather data for a given location """
    headers = {"User-Agent": "MyWeatherApp/1.0"}
    response = requests.get(f"{MET_URL}?lat={lat}&lon={lon}", headers=headers)
    return response.json()

def update_weather(locations):
    """ Updates temperature, humidity, and precipitation for a list of locations """
    print("Updating weather data...")

    data = load_weather_json()

    for city, info in locations.items():
        current_time = time.time()  # Current time in seconds since the epoch
        # Check if the weather data is already up-to-date (within 10 minutes)
        if city in data["locations"] and "weather" in data["locations"][city]:
            last_updated = data["locations"][city]["weather"]["last_updated"]
            # Convert the ISO datetime string to a timestamp (float)
            # last_updated = convert_to_timestamp(last_updated_str)
            time_diff = current_time - last_updated

            # If the data is older than 10 minutes (600 seconds), fetch new data
            if time_diff < 600:
                print(f"Weather data for {city} is recent, skipping update.")
                continue  # Skip if the data is recent enough
           
        weather_data = fetch_weather(info["lat"], info["lon"])
        
        try:
            temperature = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
            humidity = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["relative_humidity"]
            precipitation = weather_data["properties"]["timeseries"][0]["data"]["next_1_hours"]["details"]["precipitation_amount"]
        except:
            print(f"Unable to extract weather for {city}")
            continue

        # Update the data with the new weather information
        if city not in data["locations"]:
            data["locations"][city] = {}

        data["locations"][city]["weather"] = {
            "temperature": temperature,
            "humidity": humidity,
            "precipitation": precipitation,
            "last_updated": current_time  # Store current timestamp
        }

        save_json(data)


# def fetch_aqi(lat, lon):
#     """ Fetch AQI data for a given location using AirVisual API """
#     response = requests.get(f"http://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={AIRVISUAL_API_KEY}")
#     return response.json()


# def update_aqi(locations):
#     """ Updates AQI data for a list of locations using the AirVisual API """
#     print("Updating AQI data...")

#     data = load_weather_json()

#     for city, info in locations.items():
#         current_time = time.time()  # Current time in seconds since the epoch
#         # Check if the AQI data is already up-to-date (within 10 minutes)
#         if city in data["locations"] and "air_quality" in data["locations"][city]:
#             last_updated = data["locations"][city]["air_quality"]["last_updated"]
#             # Convert the ISO datetime string to a timestamp (float)
#             # last_updated = convert_to_timestamp(last_updated_str)
#             time_diff = current_time - last_updated

#             # If the data is older than 10 minutes (600 seconds), fetch new data
#             if time_diff < 600:
#                 print(f"AQI data for {city} is recent, skipping update.")
#                 continue  # Skip if the data is recent enough

#         aqi_data = fetch_aqi(info["lat"], info["lon"])
        
#         # Extract AQI value from the AirVisual response
#         try:
#             aqi_value = aqi_data["data"]["current"]["pollution"]["aqius"]
#         except KeyError:
#             print(f"Error extracting AQI for {city}")
#             continue

#         # Update the data with the new AQI information
#         if city not in data["locations"]:
#             data["locations"][city] = {}

#         data["locations"][city]["air_quality"] = {
#             "AQI": aqi_value,
#             "last_updated": current_time  # Store current timestamp
#         }

#     save_json(data)


def fetch_aqi(lat, lon):
    """ Fetch AQI data from WAQI API """
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={WAQI_API_KEY}"
    response = requests.get(url)
    return response.json()

def update_aqi(locations):
    """ Updates AQI data for a list of locations using the WAQI API """
    print("Updating AQI data...")

    data = load_weather_json()
    current_time = time.time()

    for city, info in locations.items():
        if city in data["locations"] and "air_quality" in data["locations"][city]:
            last_updated = data["locations"][city]["air_quality"]["last_updated"]
            if current_time - last_updated < 600:
                print(f"AQI data for {city} is recent, skipping update.")
                continue
            
        aqi_data = fetch_aqi(info["lat"], info["lon"])
        # print(aqi_data)
        
        try:
            aqi_value = aqi_data["data"]["aqi"]
        except:
            print(f"Error extracting AQI for {city}")
            continue

        if city not in data["locations"]:
            data["locations"][city] = {}

        data["locations"][city]["air_quality"] = {
            "AQI": aqi_value,
            "last_updated": current_time
        }

        save_json(data)





def fetch_traffic(lat, lon):
    """ Fetch traffic flow or congestion data from a traffic API (e.g., TomTom, Sygic) """
    # Example URL for TomTom Traffic API (You should replace it with actual endpoint for your API)
    # url = f"https://api.tomtom.com/traffic/services/flow/7.0/flowSegmentData?point={lat},{lon}&unit=kph&key={TRAFFIC_API_KEY}"
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json?point={lat}%2C{lon}&unit=KMPH&openLr=false&key={TRAFFIC_API_KEY}"

    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching traffic data for {lat}, {lon}")
        return None

def update_traffic(locations):
    """ Updates traffic flow data for a list of locations """
    print("Updating Traffic Flow Data...")
    data = load_weather_json()  # Assuming you have this function to load your data

    current_time = time.time()

    for city, info in locations.items():
        if city in data["locations"] and "traffic" in data["locations"][city]:
            last_updated = data["locations"][city]["traffic"]["last_updated"]
            if current_time - last_updated < 600:
                print(f"Traffic data for {city} is recent, skipping update.")
                continue  # Skip if the data is recent
            
        traffic_data = fetch_traffic(info["lat"], info["lon"])
        # Fetch traffic flow data
        

           
        # Extract congestion level or traffic flow data
        try:
            congestion_level = (traffic_data["flowSegmentData"]["freeFlowSpeed"] - traffic_data["flowSegmentData"]["currentSpeed"]) / traffic_data["flowSegmentData"]["freeFlowSpeed"]
        except ZeroDivisionError:
            congestion_level = 1.0  # Treat as completely congested if free-flow speed is zero
        except:
            print(f"Error extracting traffic for {city}")
            continue
        # congestion_level = (traffic_data["flowSegmentData"]["freeFlowSpeed"] - traffic_data["flowSegmentData"]["currentSpeed"])/traffic_data["flowSegmentData"]["freeFlowSpeed"]
        # You could use other parameters like "freeFlowSpeed" or "congestion" if available

        # Update the data with new traffic information
        if city not in data["locations"]:
            data["locations"][city] = {}

        data["locations"][city]["traffic"] = {
            "congestion_level": congestion_level,  # Speed or congestion level (in km/h, or you can convert to other units)
            "last_updated": current_time
        }

        save_json(data)  # Save the updated data




def load_weather_json():
    """ Loads the existing data from the JSON file """
    try:
        with open("pilot_weather.json", "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Failed to load API data")
        return {}  # Return empty dict to maintain consistency
    except FileNotFoundError:
        return {"locations": {}}  # Initialize with an empty dictionary if the file doesn't exist
    

def save_json(data):
    """ Saves the updated data (weather & AQI) to a JSON file """
    with open("pilot_weather.json", "w") as f:
        json.dump(data, f, indent=4)
    print("JSON updated!")

def convert_to_timestamp(last_updated_str):
    """ Converts an ISO datetime string to a timestamp (float) """
    try:
        dt_object = datetime.strptime(last_updated_str, "%Y-%m-%dT%H:%M:%SZ")  # Parse string into datetime object
        return dt_object.timestamp()  # Convert to timestamp (float)
    except ValueError:
        return 0  # If conversion fails, return 0 (or handle however you prefer)



def value_to_color(data):
    # Currently normalizes on indicator range but perhaps should be changed
    latest_entry = max(data, key=lambda x: list(x.keys())[0])
    latest_date, latest_value = list(latest_entry.items())[0]
    values = [list(entry.values())[0] for entry in data]
    # print(latest_date, latest_value)
    
    # Get the latest value
    # latest_value = values[-1]
    
    # Determine the range
    min_value = min(values)
    max_value = max(values)
    
    # Normalize the latest value between 0 and 1
    normalized_value = (latest_value - min_value) / (max_value - min_value)
    
    if normalized_value <= 0.25:
        # Red to Orange (0.0 - 0.25)
        red = 255
        green = int(normalized_value * 4 * 127)  # Gradually increase green
        blue = 0
    elif normalized_value <= 0.5:
        # Orange to Yellow (0.25 - 0.5)
        red = 255
        green = int(127 + (normalized_value - 0.25) * 4 * 128)  # Max at 255
        blue = 0
    elif normalized_value <= 0.75:
        # Yellow to Bright Green (0.5 - 0.75)
        red = int(255 - (normalized_value - 0.5) * 4 * 255)  # Gradually decrease red
        green = 255
        blue = 0
    else:
        # Bright Green to Dark Green (0.75 - 1.0)
        red = 0
        green = int(255 - (normalized_value - 0.75) * 4 * 128)  # Gradually decrease green
        blue = 0
    
    return f"rgb({red}, {green}, {blue})"


def average_color(colors):
    """
    Calculate the average color from a list of colors in the format f"rgb(r, g, b)".
    
    Args:
    - colors (list of str): List of color strings in f"rgb(r, g, b)" format.
    
    Returns:
    - str: The average color in f"rgb(r, g, b)" format.
    """
    # Function to extract RGB values from the color string
    def extract_rgb(color):
        # Use regex to extract r, g, b from the format f"rgb(r, g, b)"
        match = re.match(r"rgb\((\d+), (\d+), (\d+)\)", color)
        if match:
            return tuple(map(int, match.groups()))
        return None

    # Extract all RGB values from the colors list
    rgb_values = [extract_rgb(color) for color in colors]

    # Calculate the average of each color channel
    avg_r = sum(r for r, g, b in rgb_values) / len(rgb_values)
    avg_g = sum(g for r, g, b in rgb_values) / len(rgb_values)
    avg_b = sum(b for r, g, b in rgb_values) / len(rgb_values)

    # Construct the average RGB color in the format f"rgb(r, g, b)"
    avg_color = f"rgb({int(avg_r)}, {int(avg_g)}, {int(avg_b)})"
    
    return avg_color

# Convert the file to a downloadable format
def get_binary_file(file_path):
    with open(file_path, "rb") as f:
        return f.read()

def load_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
    
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
    

def filter_pilots_by_category(pilot_df, filter_string):
    """
    Filters pilots based on a given thematic cluster or impact area.
    
    Parameters:
    df (DataFrame): The DataFrame containing pilot data.
    filter_string (str): The category (either a thematic cluster or an impact area) to filter by.

    Returns:
    df: A dataframe of the filtered rows
    """
    # Ensure both thematic clusters and impact areas are treated as lists
    pilot_df["Thematic Clasters"] = pilot_df["Thematic Clasters"].astype(str).str.split(", ")
    pilot_df["Impact Areas"] = pilot_df["Impact Areas"].astype(str).str.split(", ")

    # Filter rows where the filter_string appears in either column
    mask = pilot_df["Thematic Clasters"].apply(lambda x: filter_string in x) | pilot_df["Impact Areas"].apply(lambda x: filter_string in x)
    
    # Return the matching pilot names
    return pilot_df[mask]