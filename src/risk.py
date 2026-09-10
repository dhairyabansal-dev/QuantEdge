from __future__ import annotations

import numpy as np
import pandas as pd

TRADING_DAYS = 252


def max_drawdown(equity: pd.Series) -> float:
    """Return the worst peak-to-trough percentage decline."""
    equity = equity.dropna().astype(float)
    if equity.empty:
        return 0.0
    return float((equity / equity.cummax() - 1.0).min())


def _validate_alpha(alpha: float) -> None:
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be between 0 and 1")


def var_historical(returns: pd.Series, alpha: float = 0.95) -> float:
    """Historical one-period Value at Risk, expressed as a positive loss."""
    _validate_alpha(alpha)
    returns = returns.dropna().astype(float)
    if returns.empty:
        return 0.0
    return float(max(0.0, -returns.quantile(1.0 - alpha)))


def cvar_historical(returns: pd.Series, alpha: float = 0.95) -> float:
    """Historical expected shortfall beyond the VaR threshold."""
    _validate_alpha(alpha)
    returns = returns.dropna().astype(float)
    if returns.empty:
        return 0.0

    var = var_historical(returns, alpha)
    if var == 0.0:
        losses = returns[returns < 0]
        return float(-losses.mean()) if not losses.empty else 0.0

    tail = returns[returns <= -var]
    return float(-tail.mean()) if not tail.empty else var


def metrics(returns: pd.Series, equity: pd.Series) -> dict[str, float]:
    """Calculate annualized performance and downside-risk statistics."""
    returns = returns.dropna().astype(float)
    equity = equity.dropna().astype(float)
    if returns.empty or equity.empty:
        raise ValueError("returns and equity must contain at least one observation")

    mean_return = returns.mean()
    volatility = returns.std(ddof=1)
    sharpe = np.sqrt(TRADING_DAYS) * mean_return / volatility if volatility > 0 else 0.0

    negative_returns = returns.clip(upper=0.0)
    downside_deviation = np.sqrt(np.mean(negative_returns**2))
    sortino = (
        np.sqrt(TRADING_DAYS) * mean_return / downside_deviation
        if downside_deviation > 0
        else 0.0
    )

    mdd = max_drawdown(equity)
    years = max(len(returns) / TRADING_DAYS, 1 / TRADING_DAYS)
    cagr = float(equity.iloc[-1] ** (1.0 / years) - 1.0) if equity.iloc[-1] > 0 else -1.0
    calmar = cagr / abs(mdd) if mdd < 0 else 0.0

    return {
        "Total Return": float(equity.iloc[-1] - 1.0),
        "CAGR": cagr,
        "Annual Volatility": float(volatility * np.sqrt(TRADING_DAYS)),
        "Sharpe": float(sharpe),
        "Sortino": float(sortino),
        "Calmar": float(calmar),
        "Max Drawdown": float(mdd),
        "VaR 95%": var_historical(returns),
        "CVaR 95%": cvar_historical(returns),
    }
