import numpy as np
import pandas as pd

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    close = df["close"].values

    # Simple Moving Average (20-day)
    df["sma_20"] = df["close"].rolling(window=20).mean()

    # Exponential Moving Average (20-day)
    df["ema_20"] = df["close"].ewm(span=20, adjust=False).mean()

    # Daily log returns
    log_returns = np.diff(np.log(close))

    # Rolling 20-day annualized volatility
    vol = pd.Series(log_returns, index=df.index[1:])
    df["volatility"] = vol.rolling(20).std() * np.sqrt(252) * 100  # in %

    # RSI (14-day)
    delta = df["close"].diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    rs    = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    return df