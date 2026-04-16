from sqlalchemy import create_engine, text
DB_URL = "mysql+mysqlconnector://root:password@localhost/stock_db"
engine = create_engine(DB_URL)


with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            ticker      VARCHAR(10),
            date        DATE,
            open        FLOAT,
            high        FLOAT,
            low         FLOAT,
            close       FLOAT,
            volume      BIGINT,
            sma_20      FLOAT,
            ema_20      FLOAT,
            volatility  FLOAT,
            UNIQUE KEY unique_ticker_date (ticker, date)
        )
    """))
    conn.commit()
