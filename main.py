from fetcher import fetch_and_clean
from indicators import add_indicators
from db_setup import engine, store_to_db
from charts import plot_analysis

tickers = ["AAPL", "TSLA", "MSFT"]

try:
    for ticker in tickers:
        print(f"Processing {ticker}...")
        # 1. Fetch raw data
        df = fetch_and_clean(ticker, period="1y") 
        # 2. CALCULATE indicators (This adds sma_20, ema_20, etc.)
        df = add_indicators(df) 
        # 3. Store the PROCESSED data to the database
        store_to_db(df, engine) 
        # 4. Show the chart for this ticker
        plot_analysis(df, ticker)

    print("--- Done. All tickers processed and stored in MySQL. ---")
except Exception as e:
    print(f"FAILED: {e}")