import datetime as dt

import plotly.graph_objects as go
import streamlit as st

from src.data import load_prices
from src.signals import make_signals
from src.backtest import run_backtest
from src.risk import metrics

st.set_page_config(page_title="QuantEdge", page_icon="Q", layout="wide")
st.title("QuantEdge")
st.caption("End-to-end quantitative research: data → signal → backtest → risk")

with st.sidebar:
    ticker = st.text_input("Ticker", "SPY").upper().strip()
    start = st.date_input("Start", dt.date(2018, 1, 1))
    end = st.date_input("End", dt.date.today())
    fee = st.slider("Fee (bps)", 0.0, 30.0, 5.0, 0.5)
    slip = st.slider("Slippage (bps)", 0.0, 30.0, 2.0, 0.5)
    fast = st.slider("Momentum fast", 5, 30, 12)
    slow = st.slider("Momentum slow", 30, 150, 50)
    run = st.button("Run Research", type="primary", use_container_width=True)

if run or "result" not in st.session_state:
    try:
        prices = load_prices(ticker, str(start), str(end))
        signals = make_signals(prices, fast, slow)
        result = run_backtest(prices["Close"], signals["signal"], fee, slip)
        st.session_state.result = result
        st.session_state.ticker = ticker
    except Exception as exc:
        st.error(f"Research run failed: {exc}")
        st.stop()

result = st.session_state.result
m = metrics(result["strategy_return"], result["equity"])
cols = st.columns(6)
for col, (label, value) in zip(cols, [("Total Return", m["Total Return"]), ("CAGR", m["CAGR"]), ("Sharpe", m["Sharpe"]), ("Sortino", m["Sortino"]), ("Max DD", m["Max Drawdown"]), ("CVaR", m["CVaR 95%"]) ]):
    col.metric(label, f"{value:.2%}" if label not in {"Sharpe", "Sortino"} else f"{value:.2f}")

st.subheader(f"Equity Curve — {st.session_state.ticker}")
fig = go.Figure()
fig.add_trace(go.Scatter(x=result.index, y=result["equity"], name="Strategy"))
fig.add_trace(go.Scatter(x=result.index, y=result["benchmark"], name="Buy & Hold"))
fig.update_layout(height=430, yaxis_title="Growth of $1", xaxis_title="Date", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Drawdown")
    dd = result["equity"] / result["equity"].cummax() - 1
    st.area_chart(dd)
with right:
    st.subheader("Position & Turnover")
    st.line_chart(result[["position", "turnover"]])

with st.expander("Full risk report"):
    st.dataframe({k: [v] for k, v in m.items()}, use_container_width=True)
