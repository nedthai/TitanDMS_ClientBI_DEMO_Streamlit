import duckdb
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DUCKDB_PATH", "data/Database_Data.duckdb")

def get_connection():
    """Establish a connection to the DuckDB database."""
    return duckdb.connect(database=DB_PATH, read_only=True)

def execute_query(sql_query: str) -> pd.DataFrame:
    """Execute a SQL query and return a Pandas DataFrame."""
    conn = get_connection()
    try:
        df = conn.execute(sql_query).df()
        return df
    finally:
        conn.close()

def get_schema_info():
    """Get basic schema information for the LLM context."""
    conn = get_connection()
    try:
        tables = conn.execute("SHOW TABLES").df()
        schema_info = {}
        for table_name in tables['name']:
            columns = conn.execute(f"DESCRIBE {table_name}").df()
            schema_info[table_name] = columns[['column_name', 'column_type']].to_dict(orient='records')
        return schema_info
    finally:
        conn.close()
