from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
import pandas as pd
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

db_pass = quote_plus(os.getenv("DB_PASSWORD"))
engine = create_engine(f"mysql+mysqlconnector://root:{db_pass}@localhost:3306/stock_db")

@app.get("/")
def home(request: Request, ticker: str = "AAPL"):
    # Change ORDER BY to ASC so the chart draws from left to right
    query = f"SELECT * FROM stock_prices WHERE ticker = '{ticker}' ORDER BY date ASC LIMIT 100"
    df = pd.read_sql(query, engine)
    
    data = df.to_dict(orient="records")
    return templates.TemplateResponse("index.html", {"request": request, "stocks": data, "ticker": ticker})

@app.get("/favicon.ico")
async def favicon():
    return Response(content="", media_type="image/x-icon")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
