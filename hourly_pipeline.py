import requests
import psycopg
import json
import os
from dotenv import load_dotenv

# Load environment variables (like DB_USER, DB_PASSWORD) from a .env file

# --- ROBUST PATH RESOLUTION ---
# This calculates the folder where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))
# This creates a safe, OS-agnostic path to your .env file
env_path = os.path.join(script_dir, '.env')

# Now load the environment variables using that specific path
load_dotenv(dotenv_path=env_path)
# ---------------------------------------

DB_PASS = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")

def run_pipeline():
    """
    Main pipeline function: Fetches weather data from an API 
    and saves it to a PostgreSQL database.
    """
    try:
        # 1. Acquire Data from Open-Meteo API
        api_url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m"
        response = requests.get(api_url)
        payload = response.json()

        # Extract data lists from the JSON response
        times = payload["hourly"]["time"]
        temps = payload["hourly"]["temperature_2m"]

        # 2. Database Connection Configuration
        # Note: 127.0.0.1 refers to your local machine
        conn_str = {
                            "dbname": "postgres",
                            "user": DB_USER,
                            "password": DB_PASS,
                            "host": "127.0.0.1",
                            "port": "5432"
                        }

        # Using 'with' automatically closes the connection when finished
        with psycopg.connect(**conn_str) as conn:
            with conn.cursor() as cursor:
                
                # Ensure the target table exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS va_bene (
                        temperature FLOAT, 
                        forecast_time TIMESTAMP
                    )
                """)

                # WIPE the old data here
                # This ensures every time the script runs, it starts fresh
                cursor.execute("TRUNCATE TABLE va_bene;")
                
                # Insert data rows one by one
                for time_val, temp_val in zip(times, temps):
                    cursor.execute("""
                        INSERT INTO va_bene (temperature, forecast_time) 
                        VALUES (%s, %s)
                    """, (temp_val, time_val))
                
                # Commit saves the changes to the database
                conn.commit()
                print("Values inserted successfully!")

    except Exception as error:
        # Catch and print any errors (like connection issues)
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    run_pipeline()
