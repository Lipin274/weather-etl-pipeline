import os  # Native Python library to talk to your operating system
import requests
import psycopg  # Modern psycopg3 driver
from datetime import datetime
from dotenv import load_dotenv  # Import the dotenv library

# --- BULLETPROOF PATH FIX ---
# 1. Get the exact folder where this hourly_pipeline.py file lives
script_dir = os.path.dirname(os.path.abspath(__file__))
# 2. Point directly to the .env file in that exact folder
env_path = os.path.join(script_dir, '.env')
# 3. Force-load it explicitly
load_dotenv(dotenv_path=env_path)
# ----------------------------

# Grab the secret password safely out of memory
db_pass = os.getenv("DB_PASSWORD")

if not db_pass:
    print(f"CRITICAL ERROR: Could not read DB_PASSWORD from the .env file.")
    print(f"Looking for it at: {env_path}")
    print("Please check your filename and formatting!")

# Dynamic connection string using your hidden password variable
DB_PARAMS = f"dbname=postgres user=postgres password={db_pass} host=127.0.0.1 port=5432"

# The exact Open-Meteo link you generated
API_URL = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m&models=meteofrance_seamless&forecast_days=4"

def run_hourly_pipeline():
    if not db_pass:
        return
        
    try:
        print("Extracting hourly forecast data from Open-Meteo...")
        response = requests.get(API_URL)
        
        if response.status_code != 200:
            print(f"Failed to fetch data. Status: {response.status_code}")
            return
            
        payload = response.json()
        print("Extraction complete!")

        # ---- TRANSFORM LAYER ----
        hourly_data = payload.get("hourly", {})
        timestamps = hourly_data.get("time", [])          
        temperatures = hourly_data.get("temperature_2m", []) 
        
        coords = f"Lat: {payload.get('latitude')}, Lon: {payload.get('longitude')}"
        print(f"Found {len(timestamps)} hourly records to transform and load.")

        # ---- LOAD LAYER (Using pure psycopg3 syntax) ----
        print("Connecting to local PostgreSQL database...")
        with psycopg.connect(DB_PARAMS) as conn:
            with conn.cursor() as cur:
                
                # Clean old data out so you don't keep accumulating duplicates while testing
                cur.execute("TRUNCATE TABLE public.hourly_weather;")
                
                for time_str, temp in zip(timestamps, temperatures):
                    if time_str and temp is not None:
                        parsed_time = datetime.fromisoformat(time_str)
                        
                        cur.execute("""
                            INSERT INTO public.hourly_weather 
                            (location_coords, forecast_time, temperature_2m)
                            VALUES (%s, %s, %s);
                        """, (coords, parsed_time, temp))
                
                conn.commit()
                print("All hourly records successfully loaded into your database using psycopg3!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_hourly_pipeline()