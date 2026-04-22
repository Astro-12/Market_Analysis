import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from charts import plot_analysis  # Ensure this import is here

# --- 1. DATABASE CONNECTION ---
load_dotenv()
raw_pass = os.getenv("DB_PASSWORD")
if raw_pass is None:
    st.error("DB_PASSWORD not found in .env file!")
    st.stop()

db_pass = quote_plus(raw_pass)
engine = create_engine(f"mysql+mysqlconnector://root:{db_pass}@localhost/stock_db")

# --- 2. SIDEBAR SETTINGS ---
st.title("Stock Price Scanner")
st.sidebar.header("Scanner Parameters")

selected_ticker = st.sidebar.selectbox("Choose Ticker", ["AAPL", "TSLA", "MSFT"])

# Set these to more "open" default values so data shows up immediately
sma_val = st.sidebar.slider("SMA Period", 5, 200, 20)
# Raise this to 70 so you don't filter out normal price action
rsi_limit = st.sidebar.slider("RSI Threshold (Show below)", 10, 100, 70) 
# Lower this to 0.01 because stock volatility is usually very small
vol_threshold = st.sidebar.slider("Volatility Threshold (Show above)", 0.00, 1.0, 0.01, step=0.01)

# --- 3. THE "GUARANTEED DATA" QUERY ---
# We fetch all data for the selected ticker to ensure the chart always has points to plot
query = f"SELECT * FROM stock_prices WHERE ticker = '{selected_ticker}' ORDER BY date ASC"

st.subheader(f"Results for {selected_ticker}")

try:
    df = pd.read_sql(query, engine)
    if not df.empty:
        # Show the most recent stats
        st.metric("Latest Close", f"${df['close'].iloc[-1]:.2f}")
        # This will now trigger your chart on the website
        plot_analysis(df, selected_ticker)
        # Show the raw data table
        st.dataframe(df.tail(10))
    else:
        st.warning("Database is empty for this ticker. Run main.py first!")
except Exception as e:
    st.error(f"Database Error: {e}")