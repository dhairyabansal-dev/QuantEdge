from __future__ import annotations

import pandas as pd
import yfinance as yf


def load_prices(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Download adjusted OHLCV data and return a clean daily frame."""
    df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"No market data returned for {ticker}.")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.rename(columns=str.title)
    required = ["Open", "High", "Low", "Close", "Volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df[required].dropna().sort_index()
