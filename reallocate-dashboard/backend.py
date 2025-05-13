import json
import time
import schedule
import threading  # To run scheduling in a separate thread
from fastapi import FastAPI
import uvicorn
from helper_functions import update_weather, update_aqi, update_traffic
import pandas as pd

app = FastAPI()

pilots_static_df = pd.read_excel('./static/pilot_static_data.xlsx', engine="openpyxl")
locations = {row['name']: {"lat": row['lat'], "lon": row['lon']} for index, row in pilots_static_df.iterrows()}
# Load pilot site locations
# with open("./pilot_sites.json") as f:
#     pilots = json.load(f)

# locations = {pilot['name']: {"lat": pilot['coordinates'][0], "lon": pilot['coordinates'][1]} for pilot in pilots}

# Initial data update
update_weather(locations)
update_aqi(locations)
update_traffic(locations)

# endpoint to access the pilot site json data
@app.get("/pilot_api_data")
def get_weather(site_name: str):
    try:
        """Fetch weather data for the requested location."""
        with open("./pilot_weather.json") as f2:
            pilot_weather = json.load(f2)
            return {"site": site_name, site_name: pilot_weather['locations'].get(site_name, "No data")}
    except json.JSONDecodeError:
        print("Failed to load API data")
        return {"error": "Failed to load weather data"}

   

def schedule_updates():
    """Schedule background updates for weather, AQI, and traffic data."""
    schedule.every(60).minutes.do(update_weather, locations=locations)  # Weather update (hourly)
    schedule.every(60).minutes.do(update_aqi, locations=locations)      # AQI update (hourly)
    schedule.every(15).minutes.do(update_traffic, locations=locations)  # Traffic update (every 15 mins)

    while True:
        schedule.run_pending()
        time.sleep(300)  # Wait 5 minutes before checking again

# Start the scheduler in a separate thread
def start_scheduler():
    scheduler_thread = threading.Thread(target=schedule_updates, daemon=True)
    scheduler_thread.start()

if __name__ == "__main__":
    start_scheduler()  # Start scheduling in the background
    uvicorn.run(app, host="0.0.0.0", port=8000)