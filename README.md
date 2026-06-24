# Weather Data ETL Pipeline

A lightweight, robust ETL (Extract, Transform, Load) pipeline designed to fetch real-time weather forecast data and store it in a PostgreSQL database.

## Features
* **Automated Extraction:** Fetches time-series weather data from the [Open-Meteo API](https://open-meteo.com/).
* **Data Integrity:** Implements a `TRUNCATE` pattern to ensure the database always contains the most current forecast, preventing data duplication.
* **Security First:** Uses `.env` files to manage sensitive database credentials, following industry-standard security practices.
* **Resilient Connection:** Employs Python context managers (`with` statements) to ensure reliable database connection lifecycles and resource cleanup.
* **Error Handling:** Built-in `try-except` blocks to capture and report network or database connectivity issues.

## Technical Stack
* **Language:** Python
* **Database:** PostgreSQL
* **Libraries:** `psycopg` (driver), `requests` (API integration), `python-dotenv` (environment configuration)

## How it Works
The pipeline extracts forecast data from the Open-Meteo API using the `requests` library. It then parses the JSON response and performs a `TRUNCATE` operation on the PostgreSQL table before inserting the fresh dataset to ensure data accuracy and prevent record duplication.

## Setup Instructions

\### 1. Clone the project

```bash

git clone \[https://github.com/Lipin274/weather-etl-pipeline.git](https://github.com/Lipin274/weather-etl-pipeline.git)

cd weather-etl-pipeline


Install dependencies:


pip install -r requirements.txt


Configure environment variables:

Create a .env file in the project root and add your credentials:

DB_USER=your_username
DB_PASSWORD=your_password

Run the pipeline:


python hourly\_pipeline.py
