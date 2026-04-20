import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()
db_pass = quote_plus(os.getenv("DB_PASSWORD"))
engine = create_engine(f"mysql+mysqlconnector://root:{db_pass}@localhost/stock_db")

st.title("Stock price scanner")
st.sidebar.header("Scanner settings and filters")

st.sidebar.header("Scanner Parameters")
selected_ticker = st.sidebar.selectbox("Choose Ticker", ["AAPL", "TSLA", "MSFT"])
sma_val = st.sidebar.slider("SMA Period", 5, 200, 20)
rsi_limit = st.sidebar.slider("RSI Oversold Threshold", 10, 50, 30)
vol_threshold = st.sidebar.slider("Volatility Threshold", 0.01, 10.0, 0.5, step=0.01)

query = f""" 
SELECT ticker, date, close, sma, rsi, ema, volatility
FROM stock_prices
WHERE rsi < {rsi_limit} AND volatility > {vol_threshold}
AND date = (SELECT MAX(date) FROM stock_prices)
ORDER BY volatility DESC
LIMIT 100;
"""
st.subheader(f"Stocks meeting the criteria:(RSI < {rsi_limit} AND Volatility > {vol_threshold})")
try:
    df = pd.read_sql(query, engine)
    
    if not df.empty:
        # Show specific metrics for the trader
        last_price = df['close'].iloc[-1]
        last_rsi = df['rsi'].iloc[-1]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${last_price:.2f}")
        col2.metric("Current RSI", f"{last_rsi:.1f}")
        col3.metric("Status", "BUY SIGNAL" if last_rsi < rsi_limit else "HOLD")

        # DISPLAY: The Data Table
        st.subheader(f"Historical Data for {selected_ticker}")
        st.dataframe(df.tail(10))
        
    else:
        st.warning("No data found. Please run main.py to populate the database.")

except Exception as e:
    st.error(f"Database Error: {e}")