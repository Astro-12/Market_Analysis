import pandas as pd

def add_indicators(df: pd.DataFrame):
    """
    Calculates technical indicators and adds them as new columns.
    """
    # 1. Simple Moving Average (SMA)
    df['sma_20'] = df['close'].rolling(window=20).mean()
    
    # 2. Exponential Moving Average (EMA)
    df['ema_20'] = df['close'].ewm(span=20, adjust=False).mean()
    
    # 3. Volatility (Standard Deviation of returns)
    df['volatility'] = df['close'].pct_change().rolling(window=20).std()
    
    # 4. Relative Strength Index (RSI)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    return df.dropna()