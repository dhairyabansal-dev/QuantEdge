import numpy as np
import pandas as pd
import pytest

from src.backtest import run_backtest
from src.portfolio import volatility_target_weight
from src.risk import cvar_historical, max_drawdown, metrics, var_historical
from src.signals import make_signals


def test_backtest_lags_signal_and_exposure():
    close = pd.Series([100.0, 110.0, 121.0])
    signal = pd.Series([1.0, 0.0, 0.0])
    exposure = pd.Series([0.5, 0.5, 0.5])

    result = run_backtest(close, signal, fee_bps=0, slippage_bps=0, exposure=exposure)

    assert np.isclose(result.iloc[1]["strategy_return"], 0.05)
    assert np.isclose(result.iloc[2]["strategy_return"], 0.0)
    assert np.isclose(result.iloc[1]["position"], 0.5)


def test_max_drawdown():
    equity = pd.Series([1.0, 1.2, 1.0, 1.1])
    assert np.isclose(max_drawdown(equity), -1 / 6)


def test_tail_risk_positive():
    returns = pd.Series([-0.10, -0.05, 0.01, 0.02, 0.03])
    assert var_historical(returns) > 0
    assert cvar_historical(returns) >= var_historical(returns)


def test_volatility_target_has_warmup_and_cap():
    returns = pd.Series(np.linspace(-0.01, 0.01, 30))
    weights = volatility_target_weight(returns, target_vol=0.15, lookback=20, max_leverage=1.0)
    assert weights.iloc[:19].eq(0).all()
    assert weights.max() <= 1.0


def test_signal_parameters_are_validated():
    prices = pd.DataFrame({"Close": np.arange(1.0, 61.0)})
    with pytest.raises(ValueError):
        make_signals(prices, fast=50, slow=20)


def test_sortino_uses_downside_deviation():
    returns = pd.Series([-0.02, 0.01, 0.03, -0.01, 0.02])
    equity = (1.0 + returns).cumprod()
    result = metrics(returns, equity)
    expected_downside = np.sqrt(np.mean(np.array([-0.02, 0.0, 0.0, -0.01, 0.0]) ** 2))
    expected_sortino = np.sqrt(252) * returns.mean() / expected_downside
    assert np.isclose(result["Sortino"], expected_sortino)
