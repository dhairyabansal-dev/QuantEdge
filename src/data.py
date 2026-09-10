from __future__ import annotations

import pandas as pd
import yfinance as yf

REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def load_prices(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Download adjusted daily OHLCV data and return a validated DataFrame."""
    ticker = ticker.strip().upper()
    if not ticker:
        raise ValueError("Ticker cannot be empty")
    if start >= end:
        raise ValueError("start must be earlier than end")

    df = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
        group_by="column",
    )
    if df.empty:
        raise ValueError(f"No market data returned for {ticker}.")

    if isinstance(df.columns, pd.MultiIndex):
        # yfinance can return a ticker level even for a single instrument.
        df.columns = df.columns.get_level_values(0)

    df.columns = [str(column).title() for column in df.columns]
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    result = df[REQUIRED_COLUMNS].copy()
    result = result.apply(pd.to_numeric, errors="coerce")
    result = result.dropna().sort_index()
    result = result[~result.index.duplicated(keep="last")]

    if result.empty:
        raise ValueError(f"No valid rows remain after cleaning {ticker} data.")

    return result
