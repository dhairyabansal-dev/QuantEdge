from __future__ import annotations

import pandas as pd


def volatility_target_weight(returns: pd.Series, target_vol: float = 0.15, lookback: int = 20) -> pd.Series:
    """Scale exposure toward an annualized volatility target and cap leverage at 1x."""
    vol = returns.rolling(lookback).std() * (252 ** 0.5)
    return (target_vol / vol.replace(0, pd.NA)).clip(lower=0, upper=1).fillna(0.0)


def position_series(backtest: pd.DataFrame, target_vol: float = 0.15) -> pd.Series:
    weights = volatility_target_weight(backtest["asset_return"], target_vol)
    return backtest["position"] * weights
