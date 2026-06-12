\# weather-etl-pipeline



`weather-etl-pipeline` is a Python-based data engineering script that extracts hourly weather forecasts from an external REST API, cleans the records, and stores them in a local PostgreSQL database.



The script is built using modern asynchronous-capable database drivers and is structured to handle configuration variables securely.



\---



\## 🛠️ Requirements



\* \*\*Language:\*\* Python 3.x

\* \*\*Database:\*\* PostgreSQL instance (local or remote)

\* \*\*Libraries:\*\* `psycopg` (psycopg3), `requests`, `python-dotenv`



\---



\## 🚀 How it Works



The pipeline executes a classic three-step ETL lifecycle:



1\. \*\*Extract:\*\* Hits the Open-Meteo API endpoint to fetch 4 days of hourly temperature forecast data.

2\. \*\*Transform:\*\* Parses the raw JSON payload, isolates geospatial coordinates, and maps each timestamp to its temperature value.

3\. \*\*Load:\*\* Connects to PostgreSQL using a context manager and saves the rows. It runs a `TRUNCATE` command before loading to prevent duplicate rows during testing.



\### Design features:

\* \*\*Environment variables:\*\* Uses `python-dotenv` to pull database passwords from a local `.env` file so secrets are never committed to Git.

\* \*\*Absolute pathing:\*\* Resolves directory paths dynamically using `os.path.abspath(\_\_file\_\_)`. This ensures the script executes correctly when run by automated system task schedulers.

\* \*\*Resource management:\*\* Utilizes Python `with` blocks to guarantee database connections close safely even if a runtime exception occurs.



\---



\## 📥 Setup and Installation



\### 1. Clone the project

```bash

git clone \[https://github.com/Lipin274/weather-etl-pipeline.git](https://github.com/Lipin274/weather-etl-pipeline.git)

cd weather-etl-pipeline


Install dependencies:


pip install -r requirements.txt


Configure environment variables:

DB\_PASSWORD=your\_postgres\_password


Initialize database schema:

CREATE TABLE public.hourly\_weather (

&#x20;   id SERIAL PRIMARY KEY,

&#x20;   location\_coords VARCHAR(100),

&#x20;   forecast\_time TIMESTAMP,

&#x20;   temperature\_2m NUMERIC

);

Run the pipeline:


python hourly\_pipeline.py

