import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pathlib import Path

# --- CONFIGURATION ---
# Change this variable to the name of the table you want to delete
TABLE_TO_DROP = "stock_prices" 
# ---------------------

# Load credentials from .env
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
db_pass = os.getenv("DB_PASSWORD")

if not db_pass:
    raise ValueError("DB_PASSWORD not found in .env file!")

# Encode password to handle special characters like '!' or '&'
db_pass_encoded = quote_plus(db_pass)

# Connect to the stock_db
engine = create_engine(f"mysql+mysqlconnector://root:{db_pass_encoded}@localhost/stock_db")

def reset_table(table_name):
    """Drops the specified table from the database."""
    try:
        with engine.connect() as conn:
            print(f"Attempting to drop table: {table_name}...")
            # Using f-string for the table name in the command
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            conn.commit()
            print(f"SUCCESS: Table '{table_name}' has been removed.")
            print("You can now run your setup and main scripts to recreate it.")
    except Exception as e:
        print(f"ERROR: Could not drop table. {e}")

if __name__ == "__main__":
    reset_table(TABLE_TO_DROP)
