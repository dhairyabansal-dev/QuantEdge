from __future__ import annotations

import pandas as pd


def make_signals(
    prices: pd.DataFrame,
    fast: int = 12,
    slow: int = 50,
    z_window: int = 20,
    z_entry: float = -1.0,
) -> pd.DataFrame:
    """Create interpretable long/flat momentum and mean-reversion signals."""
    if fast < 1 or slow <= fast:
        raise ValueError("Require 1 <= fast < slow")
    if z_window < 2:
        raise ValueError("z_window must be at least 2")

    close = prices["Close"].astype(float)
    fast_return = close.pct_change(fast)
    slow_return = close.pct_change(slow)
    momentum = (fast_return > slow_return).fillna(False)

    rolling_mean = close.rolling(z_window, min_periods=z_window).mean()
    rolling_std = close.rolling(z_window, min_periods=z_window).std(ddof=1)
    zscore = (close - rolling_mean) / rolling_std.replace(0, pd.NA)
    mean_reversion = zscore.lt(z_entry).fillna(False)

    signal = (momentum | mean_reversion).astype(float)

    return pd.DataFrame(
        {
            "close": close,
            "fast_return": fast_return,
            "slow_return": slow_return,
            "momentum": momentum.astype(int),
            "zscore": zscore,
            "mean_reversion": mean_reversion.astype(int),
            "signal": signal,
        },
        index=prices.index,
    )
