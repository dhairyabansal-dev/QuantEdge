from __future__ import annotations

import numpy as np
import pandas as pd


def run_backtest(close: pd.Series, signal: pd.Series, fee_bps: float = 5.0, slippage_bps: float = 2.0) -> pd.DataFrame:
    """Long/flat backtest with lagged execution and proportional trading costs."""
    ret = close.pct_change().fillna(0.0)
    position = signal.shift(1).fillna(0.0)
    turnover = position.diff().abs().fillna(position.abs())
    costs = turnover * (fee_bps + slippage_bps) / 10_000
    strategy_ret = position * ret - costs
    equity = (1.0 + strategy_ret).cumprod()
    benchmark = (1.0 + ret).cumprod()
    return pd.DataFrame({"asset_return": ret, "position": position, "turnover": turnover, "cost": costs, "strategy_return": strategy_ret, "equity": equity, "benchmark": benchmark}, index=close.index)
