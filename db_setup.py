import os
import pandas as pd
from sqlalchemy import create_engine, text
import mysql.connector
import dotenv
from urllib.parse import quote_plus
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")\

db_pass = quote_plus(os.getenv("DB_PASSWORD"))

db_pass = os.getenv("DB_PASSWORD")

if db_pass is None:
    raise ValueError("DB_PASSWORD not found in .env file!")

#db_pass = "Luciferisdevil15!&"   
print(f"DEBUG password: '{db_pass}'")

# --- STEP 2: CONNECT TO THE SERVER ---
# We use 'localhost' and 'root' which are standard for local MySQL
db_pass_encoded = quote_plus(db_pass)
BASE_URL = f"mysql+mysqlconnector://root:{db_pass}@localhost"
base_engine = create_engine(BASE_URL)

try:
    with base_engine.connect() as conn:
        # Create the database if it doesn't exist yet
        conn.execute(text("CREATE DATABASE IF NOT EXISTS stock_db"))
        conn.commit()
        print("SUCCESS: Connected to MySQL and 'stock_db' is ready.")
except Exception as e:
    print(f" CONNECTION ERROR: {e}")
    print("Double-check your password and ensure MySQL is running.")

# --- STEP 3: SETUP THE TABLE ---
engine = create_engine(f"{BASE_URL}/stock_db")

with engine.connect() as conn:
    # In db_setup.py, update the CREATE TABLE section:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            ticker      VARCHAR(10),
            date        DATE,
            open        FLOAT,
            high        FLOAT,
            low         FLOAT,
            close       FLOAT,
            volume      BIGINT,
            sma         FLOAT,  -- Generic name for dynamic periods
            ema         FLOAT,  -- Generic name for dynamic periods
            rsi         FLOAT,  -- Essential for your new scanner
            volatility  FLOAT,
            UNIQUE KEY unique_ticker_date (ticker, date)
        )
    """))
    conn.commit()

def store_to_db(df: pd.DataFrame, db_engine):
    """Saves data to the MySQL table."""
    # Only keep the columns that match our SQL table
    cols = ["ticker", "open", "high", "low", "close", "volume", "sma", "ema", "rsi", "volatility"]
    df_to_save = df[cols].copy()
    df_to_save.index.name = "date"
    
    df_to_save.to_sql(
        "stock_prices",
        con=db_engine,
        if_exists="append",
        index=True
    )
    print(f"Data for {df['ticker'].iloc[0]} stored successfully.")

