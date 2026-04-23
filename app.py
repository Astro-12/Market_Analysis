import pandas as pd
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# 1. Load your .env file
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 2. Hardcode or ensure these match your .env exactly
from urllib.parse import quote_plus
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = quote_plus(os.getenv('DB_PASSWORD', ''))  # encodes !& safely
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'stock_db')

DB_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DB_URL)

@app.get("/")
def home(request: Request, ticker: str = "AAPL"):
    try:
        query = f"SELECT * FROM stock_prices WHERE ticker = '{ticker}' ORDER BY date ASC"
        df = pd.read_sql(query, engine)

        if df.empty:
            return templates.TemplateResponse("index.html", {
                "request": request, "stocks": [], "ticker": ticker
            })

        # FIX 1: Flatten MultiIndex columns if they exist
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(str(c) for c in col).strip('_') for col in df.columns]

        # FIX 2: Reset index so date isn't a tuple key
        df = df.reset_index(drop=True)

        # FIX 3: Convert date + any Timestamp columns to plain strings
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime('%Y-%m-%d')

        # FIX 4: Replace NaN with None so JSON serializes cleanly
        df = df.where(pd.notnull(df), None)

        data = df.to_dict(orient="records")

        return templates.TemplateResponse("index.html", {
            "request": request,
            "stocks": data,
            "ticker": ticker
        })

    except Exception as e:
        print(f"DATABASE ERROR: {e}")
        return {"error": str(e)}