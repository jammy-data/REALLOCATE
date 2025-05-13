### To install

1. git clone https://github.com/V-for-Vaggelis/reallocate-dashboard.git

### To run with docker (Recommended)

1. Build the image: `docker build -t reallocate-dashboard .`
2. If you obtained API keys, start the container as: `docker run --env-file .env -p 8000:8000 -p 8501:8501 reallocate-dashboard` to periodically update the backend data.
3. If not, start as: `docker run -p 8000:8000 -p 8501:8501 reallocate-dashboard` for a static version

### To run without docker

1. Create a new environment and activate it
2. Run `pip install -r requirements.txt`
3. For the backend: Open a terminal, activte your environment and run `python backend.py`
4. For the interface: Open a terminal, activte your environment and run `streamlit run app.py`

#### NOTE: To be able succesfuly update the backend API data

Before running the application:

1. Get API keys for [WAQI](https://aqicn.org/data-platform/token/) and [TomTom](https://developer.tomtom.com/user/register?destination=/how-to-get-tomtom-api-key)
2. Add their values in the WAQI_API_KEY and TRAFFIC_API_KEY placeholders in ".env.example"
3. Rename the env file `cp .env.example .env`
