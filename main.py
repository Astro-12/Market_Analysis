import os
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv
from pathlib import Path

# Local imports from your project files
from fetcher import fetch_and_clean
from indicators import add_indicators
from charts import plot_analysis

# --- 1. ENVIRONMENT & DATABASE SETUP ---
# Ensures .env is loaded from the current folder
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

raw_password = os.getenv("DB_PASSWORD")

if raw_password is None:
    raise ValueError("DB_PASSWORD not found in .env file! Check your file path and name.")

# URL-encode the password to handle special characters
db_pass_encoded = quote_plus(raw_password)

# Connection string for your specific 'stock_db'
DB_URL = f"mysql+mysqlconnector://root:{db_pass_encoded}@localhost/stock_db"
engine = create_engine(DB_URL)

def store_to_db(df: pd.DataFrame, db_engine):
    """
    Saves processed data to MySQL. 
    Uses 'replace' to prevent Duplicate Entry errors.
    """
    # Columns must match your MySQL table schema
    cols = ["ticker", "open", "high", "low", "close", "volume", "sma", "ema", "volatility", "rsi"]
    
    df_to_save = df[cols].copy()
    df_to_save.index.name = "date"
    
    # 'replace' ensures we don't crash if data already exists
    df_to_save.to_sql(
        "stock_prices",
        con=db_engine,
        if_exists="replace", 
        index=True
    )
    print(f"SUCCESS: Data for {df['ticker'].iloc[0]} stored.")

# --- 2. MAIN EXECUTION LOOP ---
def main():
    tickers = ["AAPL", "TSLA", "MSFT"]
    
    print("--- Starting Market Scanner Ingestion ---")
    
    try:
        for ticker in tickers:
            df = fetch_and_clean(ticker)
            df = add_indicators(df)
            store_to_db(df, engine) 

        print("\n--- Done. All tickers processed and stored in MySQL. ---")
        
    except Exception as e:
        print(f"\nCRITICAL FAILURE: {e}")

if __name__ == "__main__":
    main()