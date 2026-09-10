from __future__ import annotations

import pandas as pd


def make_signals(prices: pd.DataFrame, fast: int = 12, slow: int = 50, z_window: int = 20) -> pd.DataFrame:
    """Create long/flat signals. Signal is lagged one bar at execution."""
    close = prices["Close"]
    momentum = close.pct_change(fast) > close.pct_change(slow)
    mean = close.rolling(z_window).mean()
    std = close.rolling(z_window).std()
    z = (close - mean) / std.replace(0, pd.NA)
    mean_reversion = z < -1.0
    signal = (momentum | mean_reversion).astype(float)
    return pd.DataFrame({"close": close, "momentum": momentum.astype(int), "zscore": z, "signal": signal}, index=prices.index)
