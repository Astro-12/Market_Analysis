<<<<<<< HEAD
import pandas as pd

def add_indicators(df, sma_period=20, ema_period=20, rsi_period=14):
    # Use generic names for database compatibility
    df['sma'] = df['close'].rolling(window=sma_period).mean()
    df['ema'] = df['close'].ewm(span=ema_period, adjust=False).mean()
    df['volatility'] = df['close'].pct_change().rolling(window=sma_period).std()
    
    # RSI Calculation with a Zero-Division Safety Net
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    
    # Replace 0 with a tiny number to prevent NaN errors in your DB
    rs = gain / loss.replace(0, 0.001) 
    df['rsi'] = 100 - (100 / (1 + rs))
    
=======
import pandas as pd

def add_indicators(df, sma_period=20, ema_period=20, rsi_period=14):
    # Use generic names for database compatibility
    df['sma'] = df['close'].rolling(window=sma_period).mean()
    df['ema'] = df['close'].ewm(span=ema_period, adjust=False).mean()
    df['volatility'] = df['close'].pct_change().rolling(window=sma_period).std()
    
    # RSI Calculation with a Zero-Division Safety Net
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    
    # Replace 0 with a tiny number to prevent NaN errors in your DB
    rs = gain / loss.replace(0, 0.001) 
    df['rsi'] = 100 - (100 / (1 + rs))
    
>>>>>>> d5c34c3 (Fixed merge conflict)
    return df.dropna()