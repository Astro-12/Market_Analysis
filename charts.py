import matplotlib.pyplot as plt
import pandas as pd

def plot_analysis(df, ticker):
    """
    Generates a technical analysis chart for the given ticker.
    """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    fig.suptitle(f"{ticker} - Technical Analysis")

    # 1. Price + Moving Averages
    ax1.plot(df.index, df["close"], label="Close", linewidth=1.2)
    ax1.plot(df.index, df["sma"], label="SMA", linestyle="--")
    ax1.plot(df.index, df["ema"], label="EMA", linestyle=":")
    ax1.set_ylabel("Price (USD)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Volume
    ax2.bar(df.index, df["volume"], color="steelblue", alpha=0.5)
    ax2.set_ylabel("Volume")
    ax2.grid(True, alpha=0.3)

    # 3. RSI
    if 'rsi' in df.columns:
        ax3.plot(df.index, df["rsi"], color="purple")
        ax3.axhline(70, color="red", linestyle="--", alpha=0.5)
        ax3.axhline(30, color="green", linestyle="--", alpha=0.5)
        ax3.set_ylabel("RSI")
        ax3.set_ylim(0, 100)
    
    plt.tight_layout()
    plt.show()
