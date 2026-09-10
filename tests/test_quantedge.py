import numpy as np
import pandas as pd

from src.backtest import run_backtest
from src.risk import cvar_historical, max_drawdown, var_historical


def test_backtest_lags_signal():
    close = pd.Series([100, 110, 121], dtype=float)
    signal = pd.Series([1, 0, 0], dtype=float)
    result = run_backtest(close, signal, fee_bps=0, slippage_bps=0)
    assert result.iloc[1].strategy_return == 0.10
    assert result.iloc[2].strategy_return == 0.0


def test_max_drawdown():
    equity = pd.Series([1.0, 1.2, 1.0, 1.1])
    assert np.isclose(max_drawdown(equity), -1 / 6)


def test_tail_risk_positive():
    returns = pd.Series([-0.10, -0.05, 0.01, 0.02, 0.03])
    assert var_historical(returns) > 0
    assert cvar_historical(returns) >= var_historical(returns)
