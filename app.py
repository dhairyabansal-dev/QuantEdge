import datetime as dt

import plotly.graph_objects as go
import streamlit as st

from src.backtest import run_backtest
from src.data import load_prices
from src.portfolio import volatility_target_weight
from src.risk import metrics
from src.signals import make_signals

st.set_page_config(page_title="QuantEdge | Quant Research", page_icon="Q", layout="wide")

st.title("QuantEdge")
st.caption("Quantitative research, backtesting and risk analytics")

with st.sidebar:
    st.header("Research Configuration")
    ticker = st.text_input("Ticker", "SPY").upper().strip()
    start = st.date_input("Start date", dt.date(2018, 1, 1))
    end = st.date_input("End date", dt.date.today())

    st.subheader("Execution")
    fee = st.number_input("Commission (bps)", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
    slippage = st.number_input("Slippage (bps)", min_value=0.0, max_value=100.0, value=2.0, step=0.5)

    st.subheader("Signal")
    fast = st.slider("Fast momentum window", 5, 30, 12)
    slow = st.slider("Slow momentum window", 31, 150, 50)
    z_window = st.slider("Mean-reversion window", 10, 100, 20)
    z_entry = st.slider("Mean-reversion z-entry", -3.0, 0.0, -1.0, 0.1)

    st.subheader("Risk Targeting")
    target_vol = st.slider("Target annual volatility", 0.05, 0.40, 0.15, 0.01)
    max_leverage = st.slider("Maximum exposure", 0.25, 2.00, 1.00, 0.05)

    run = st.button("Run Research", type="primary", use_container_width=True)

if run or "result" not in st.session_state:
    if start >= end:
        st.error("Start date must be earlier than end date.")
        st.stop()

    try:
        prices = load_prices(ticker, str(start), str(end))
        signals = make_signals(prices, fast, slow, z_window, z_entry)
        exposure = volatility_target_weight(
            prices["Close"].pct_change().fillna(0.0),
            target_vol=target_vol,
            lookback=z_window,
            max_leverage=max_leverage,
        )
        result = run_backtest(
            prices["Close"],
            signals["signal"],
            fee_bps=fee,
            slippage_bps=slippage,
            exposure=exposure,
        )
        st.session_state.result = result
        st.session_state.ticker = ticker
        st.session_state.config = {
            "fast": fast,
            "slow": slow,
            "z_window": z_window,
            "z_entry": z_entry,
            "target_vol": target_vol,
            "max_leverage": max_leverage,
        }
    except Exception as exc:
        st.error(f"Research run failed: {exc}")
        st.stop()

result = st.session_state.result
m = metrics(result["strategy_return"], result["equity"])

st.subheader(f"Research Results — {st.session_state.ticker}")

cols = st.columns(5)
summary = [
    ("CAGR", m["CAGR"], "pct"),
    ("Sharpe", m["Sharpe"], "ratio"),
    ("Sortino", m["Sortino"], "ratio"),
    ("Max Drawdown", m["Max Drawdown"], "pct"),
    ("CVaR 95%", m["CVaR 95%"], "pct"),
]
for col, (label, value, kind) in zip(cols, summary):
    formatted = f"{value:.2%}" if kind == "pct" else f"{value:.2f}"
    col.metric(label, formatted)

fig = go.Figure()
fig.add_trace(go.Scatter(x=result.index, y=result["equity"], name="QuantEdge Strategy"))
fig.add_trace(go.Scatter(x=result.index, y=result["benchmark"], name="Buy & Hold"))
fig.update_layout(
    title="Growth of $1",
    xaxis_title="Date",
    yaxis_title="Portfolio Value",
    hovermode="x unified",
    height=450,
)
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Drawdown")
    drawdown = result["equity"] / result["equity"].cummax() - 1.0
    st.line_chart(drawdown)

with right:
    st.subheader("Exposure & Turnover")
    st.line_chart(result[["position", "turnover"]])

with st.expander("Full risk report"):
    report = {key: [value] for key, value in m.items()}
    st.dataframe(report, use_container_width=True, hide_index=True)

with st.expander("Research assumptions"):
    st.json({
        "ticker": st.session_state.ticker,
        "execution_cost_bps": fee,
        "slippage_bps": slippage,
        **st.session_state.config,
    })

st.caption("Research use only. Historical backtests do not guarantee future performance.")
