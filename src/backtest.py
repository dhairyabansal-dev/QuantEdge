from __future__ import annotations

import pandas as pd


def run_backtest(
    close: pd.Series,
    signal: pd.Series,
    fee_bps: float = 5.0,
    slippage_bps: float = 2.0,
    exposure: pd.Series | None = None,
) -> pd.DataFrame:
    """Run a long/flat daily backtest with lagged execution and proportional costs."""
    if fee_bps < 0 or slippage_bps < 0:
        raise ValueError("fee_bps and slippage_bps must be non-negative")

    close = close.astype(float)
    signal = signal.reindex(close.index).astype(float)
    if exposure is None:
        exposure = pd.Series(1.0, index=close.index)
    else:
        exposure = exposure.reindex(close.index).astype(float).clip(lower=0)

    asset_return = close.pct_change().fillna(0.0)
    # Both the signal and exposure are known before the next session executes.
    position = (signal * exposure).shift(1).fillna(0.0)
    turnover = position.diff().abs().fillna(position.abs())
    trading_cost = turnover * (fee_bps + slippage_bps) / 10_000
    strategy_return = position * asset_return - trading_cost

    equity = (1.0 + strategy_return).cumprod()
    benchmark = (1.0 + asset_return).cumprod()

    return pd.DataFrame(
        {
            "asset_return": asset_return,
            "signal": signal,
            "exposure": exposure,
            "position": position,
            "turnover": turnover,
            "cost": trading_cost,
            "strategy_return": strategy_return,
            "equity": equity,
            "benchmark": benchmark,
        },
        index=close.index,
    )
