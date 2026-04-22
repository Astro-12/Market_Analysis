import yfinance as yf
import pandas as pd

def fetch_and_clean(ticker: str, period: str = "1y"):
    """
    Downloads stock data and flattens multi-index columns to prevent 'tuple' errors.
    """
    print(f"Downloading data for {ticker}...")
    df = yf.download(ticker, period=period)
    
    # FIX: Flatten multi-index columns if they exist
    if isinstance(df.columns, pd.MultiIndex):#type: ignore
        df.columns = [col[0] for col in df.columns]#type: ignore
    
    # Standardize column names to lowercase for the database
    df.columns = [str(c).lower() for c in df.columns]#type: ignore
    
    # Add the ticker column
    df["ticker"] = ticker#type: ignore
    
    return df.dropna()#type: ignore