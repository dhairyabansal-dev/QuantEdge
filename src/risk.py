from __future__ import annotations

import numpy as np
import pandas as pd


def max_drawdown(equity: pd.Series) -> float:
    return float((equity / equity.cummax() - 1).min())


def var_historical(returns: pd.Series, alpha: float = 0.95) -> float:
    return float(-returns.quantile(1 - alpha))


def cvar_historical(returns: pd.Series, alpha: float = 0.95) -> float:
    var = var_historical(returns, alpha)
    tail = returns[returns <= -var]
    return float(-tail.mean()) if not tail.empty else var


def metrics(returns: pd.Series, equity: pd.Series) -> dict[str, float]:
    returns = returns.dropna()
    ann = 252
    mean = returns.mean()
    vol = returns.std(ddof=1)
    sharpe = np.sqrt(ann) * mean / vol if vol else 0.0
    downside = returns.clip(upper=0).std(ddof=1)
    sortino = np.sqrt(ann) * mean / downside if downside else 0.0
    mdd = max_drawdown(equity)
    years = max(len(returns) / ann, 1 / ann)
    cagr = float(equity.iloc[-1] ** (1 / years) - 1)
    calmar = cagr / abs(mdd) if mdd else 0.0
    return {"Total Return": float(equity.iloc[-1] - 1), "CAGR": cagr, "Annual Volatility": float(vol * np.sqrt(ann)), "Sharpe": float(sharpe), "Sortino": float(sortino), "Calmar": float(calmar), "Max Drawdown": mdd, "VaR 95%": var_historical(returns), "CVaR 95%": cvar_historical(returns)}
