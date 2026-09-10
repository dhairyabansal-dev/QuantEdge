# QuantEdge

End-to-end quantitative trading and portfolio research platform.

QuantEdge turns market data into testable investment research through a reproducible pipeline:

`Market Data → Features → Signals → Backtest → Risk → Portfolio → Analytics → Dashboard`

## What it demonstrates
- Historical OHLCV ingestion with `yfinance`
- Momentum and mean-reversion signals
- Walk-forward-style train/test evaluation
- Transaction costs and slippage
- Position sizing and portfolio construction
- Sharpe, Sortino, Calmar, max drawdown and VaR/CVaR
- Benchmark comparison and equity/drawdown analytics
- Streamlit research dashboard
- Unit tests and CI

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Research model
The default strategy combines 12/50-day momentum with a 20-day mean-reversion filter. Signals are lagged before execution to avoid look-ahead bias. Backtests model configurable proportional transaction costs and slippage.

> This repository is an educational research system, not financial advice or a production execution engine.

## Structure

```text
QuantEdge/
├── app.py
├── src/
│   ├── data.py
│   ├── signals.py
│   ├── backtest.py
│   ├── risk.py
│   └── portfolio.py
├── tests/
│   └── test_quantedge.py
├── .github/workflows/ci.yml
└── requirements.txt
```

## Roadmap
- Factor model attribution
- Multi-asset portfolio optimization
- Regime detection
- Persistent experiment registry
- Optional broker/execution adapter
