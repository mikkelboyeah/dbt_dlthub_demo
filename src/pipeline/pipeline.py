"""dlt pipeline template for loading data into DuckDB."""

from __future__ import annotations
from pathlib import Path
import dlt
import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Use absolute path to ensure dlt places the duckdb in the sandbox, not a relative path that changes
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = PROJECT_DIR / "data" / "db.duckdb"

@dlt.resource(name="weather_oslo", write_disposition="replace")
def get_weather_data():
    """Fetch weather data for Oslo from yr.no."""
    url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.91&lon=10.75"
    headers = {
        "User-Agent": "DltHubDemo/1.0 (test@example.com)"
    }
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    # Locationforecast API returns properties.timeseries containing the forecasts
    yield response.json().get("properties", {}).get("timeseries", [])

@dlt.resource(name="pokemon", write_disposition="replace")
def get_pokemon_data():
    """Fetch a few pokemon from PokeAPI to show off nested JSON extraction."""
    # Let's get the first 10 pokemon to keep it light
    url = "https://pokeapi.co/api/v2/pokemon?limit=10"
    response = requests.get(url, verify=False)
    response.raise_for_status()
    results = response.json().get("results", [])
    
    # We yield the details for each pokemon
    for p in results:
        detail_res = requests.get(p["url"], verify=False)
        detail_res.raise_for_status()
        yield detail_res.json()

def load_data() -> None:
    """Initialize the DuckDB database and load weather and pokemon data into the raw schema."""
    # Support DB_PATH env var, falling back to default
    db_path = Path(os.environ.get("DB_PATH", DEFAULT_DB_PATH))
    
    if not db_path.exists():
        import sys
        print(f"Error: Database not found at {db_path}. Please run 'task bootstrap' first.", file=sys.stderr)
        sys.exit(1)
        
    pipeline = dlt.pipeline(
        pipeline_name="template_pipeline",
        pipelines_dir=".dlt/pipelines",  # Isolate state to project directory
        destination=dlt.destinations.duckdb(credentials={"database": str(db_path)}),
        dataset_name="raw",
    )
    
    # Run the pipeline with the sources
    info = pipeline.run([get_weather_data(), get_pokemon_data()])
    print(info)
