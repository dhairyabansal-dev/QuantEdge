# QuantEdge

### End-to-End Quantitative Research & Backtesting Platform

QuantEdge is a Python-based quantitative research platform for turning historical market data into reproducible strategy research. It combines data ingestion, signal generation, realistic backtesting, volatility-aware position sizing, performance attribution, and tail-risk analysis in a single workflow.

> **Status:** Active research project
>
> QuantEdge is designed for research and education. It is not a live trading system and does not constitute financial advice.

## Research Pipeline

```text
┌──────────────┐
│ Market Data  │  Yahoo Finance / OHLCV
└──────┬───────┘
       ↓
┌──────────────┐
│ Signal Engine│  Momentum + Mean Reversion
└──────┬───────┘
       ↓
┌──────────────┐
│ Backtest     │  Lagged execution + costs + slippage
└──────┬───────┘
       ↓
┌──────────────┐
│ Risk Engine  │  Volatility + VaR + CVaR + drawdown
└──────┬───────┘
       ↓
┌──────────────┐
│ Portfolio    │  Volatility targeting + exposure control
└──────┬───────┘
       ↓
┌──────────────┐
│ Analytics    │  CAGR + Sharpe + Sortino + Calmar
└──────┬───────┘
       ↓
┌──────────────┐
│ Dashboard    │  Interactive Streamlit research interface
└──────────────┘
```

## Why QuantEdge?

The project focuses on the parts of quantitative research that are easy to overlook in simple strategy notebooks:

- **No same-bar execution:** signals are shifted before returns are applied to reduce look-ahead bias.
- **Trading frictions:** proportional commissions and slippage are included in the backtest.
- **Risk-aware sizing:** exposure can be scaled toward a target annualized volatility.
- **Benchmarking:** strategy performance is compared with buy-and-hold.
- **Tail-risk analysis:** historical VaR and CVaR are reported alongside conventional performance metrics.
- **Reproducibility:** research parameters are exposed through the dashboard and the core engine is covered by tests.

## Strategy Framework

The baseline signal combines two interpretable components:

### Momentum

A fast/slow price-return comparison identifies positive trend persistence.

### Mean Reversion

A rolling z-score identifies unusually weak prices relative to their recent distribution.

The resulting signal is converted into a long/flat position and **lagged by one trading session before execution**.

This is intentionally a transparent baseline rather than an opaque machine-learning strategy, making it easier to inspect, test, and extend.

## Risk & Performance Metrics

QuantEdge reports:

| Category | Metrics |
|---|---|
| Returns | Total Return, CAGR |
| Risk | Annualized Volatility, Maximum Drawdown |
| Risk-adjusted | Sharpe, Sortino, Calmar |
| Tail risk | Historical VaR 95%, Historical CVaR 95% |
| Trading | Turnover, estimated transaction costs |

## Interactive Dashboard

The Streamlit application allows researchers to change:

- Asset ticker
- Backtest date range
- Commission assumptions
- Slippage assumptions
- Momentum lookback windows
- Strategy parameters

The dashboard displays the resulting equity curve, benchmark comparison, drawdown profile, position exposure, turnover, and risk report.

## Project Structure

```text
QuantEdge/
├── app.py                         # Streamlit research interface
├── src/
│   ├── __init__.py
│   ├── data.py                    # Market-data ingestion and validation
│   ├── signals.py                 # Strategy signal generation
│   ├── backtest.py                # Lagged execution and trading costs
│   ├── portfolio.py               # Volatility-targeted exposure
│   └── risk.py                    # Performance and tail-risk analytics
├── tests/
│   └── test_quantedge.py          # Core quantitative unit tests
├── .github/
│   └── workflows/
│       └── ci.yml                 # Automated test workflow
├── .gitignore
└── requirements.txt
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/dhairyabansal-dev/QuantEdge.git
cd QuantEdge
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the research dashboard

```bash
streamlit run app.py
```

### 5. Run the test suite

```bash
pytest -q
```

## Example Research Workflow

1. Select an instrument such as `SPY`.
2. Choose the historical research window.
3. Set commission and slippage assumptions.
4. Adjust momentum parameters.
5. Run the strategy.
6. Compare strategy equity against buy-and-hold.
7. Inspect drawdown, turnover and exposure.
8. Evaluate Sharpe, Sortino, Calmar, VaR and CVaR.

The framework is intentionally modular, so individual components can be replaced without rewriting the complete pipeline.

## Engineering Principles

QuantEdge follows a few principles expected in a serious research codebase:

- **Separation of concerns:** data, signals, execution, portfolio construction, and risk are isolated into modules.
- **Explicit assumptions:** trading costs and strategy parameters are configurable.
- **Testable components:** core numerical behaviour is validated with unit tests.
- **Avoid avoidable bias:** execution is separated from signal generation through lagged positions.
- **Readable research:** the baseline strategy uses interpretable mathematical rules.

## Roadmap

Planned extensions include:

- Walk-forward optimization with explicit train/test windows
- Multi-asset portfolio construction
- Mean-variance and risk-parity allocation
- Factor exposure and performance attribution
- Regime detection
- Parameter and experiment tracking
- Additional risk models, including parametric and Monte Carlo VaR
- Persistent research results and downloadable reports
- Optional broker/execution adapters

## Disclaimer

QuantEdge is a research and educational project. Historical backtests are subject to model assumptions, data limitations, transaction costs, slippage, parameter sensitivity, and other sources of uncertainty. Backtested performance does not guarantee future results.

## Author

**Dhairya Bansal**

GitHub: https://github.com/dhairyabansal-dev
