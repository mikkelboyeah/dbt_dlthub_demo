"""dlt pipeline template for loading data into DuckDB."""

from __future__ import annotations
from pathlib import Path
import dlt
import os

DEFAULT_DB_PATH = Path("data/db.duckdb")

def load_data() -> None:
    """Initialize the DuckDB database and load dummy data into the raw schema."""
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
    
    # Dummy data for validation
    data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ]
    
    pipeline.run(data, table_name="users")
