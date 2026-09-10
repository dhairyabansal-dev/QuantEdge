from __future__ import annotations

import numpy as np
import pandas as pd


def volatility_target_weight(
    returns: pd.Series,
    target_vol: float = 0.15,
    lookback: int = 20,
    max_leverage: float = 1.0,
) -> pd.Series:
    """Return exposure weights scaled toward a target annualized volatility."""
    if target_vol <= 0:
        raise ValueError("target_vol must be positive")
    if lookback < 2:
        raise ValueError("lookback must be at least 2")
    if max_leverage <= 0:
        raise ValueError("max_leverage must be positive")

    realized_vol = returns.rolling(lookback, min_periods=lookback).std(ddof=1) * np.sqrt(252)
    weight = target_vol / realized_vol.replace(0, np.nan)
    return weight.clip(lower=0, upper=max_leverage).fillna(0.0)


def apply_volatility_target(
    backtest: pd.DataFrame,
    target_vol: float = 0.15,
    lookback: int = 20,
    max_leverage: float = 1.0,
) -> pd.DataFrame:
    """Apply volatility targeting to an existing long/flat backtest."""
    required = {"asset_return", "position"}
    missing = required.difference(backtest.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    result = backtest.copy()
    result["volatility_weight"] = volatility_target_weight(
        result["asset_return"], target_vol, lookback, max_leverage
    )
    result["target_position"] = result["position"] * result["volatility_weight"]
    return result
