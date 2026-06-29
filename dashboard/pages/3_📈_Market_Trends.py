import streamlit as st
import plotly.express as px

from utils import load_coin_history

st.set_page_config(
    page_title="Market Trends",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Market Trends")

coin_history = load_coin_history()

coins = sorted(
    coin_history["coin"].unique()
)

selected_coin = st.selectbox(
    "Choose Coin",
    coins
)

df = (
    coin_history[
        coin_history["coin"] == selected_coin
    ]
    .sort_values("timestamp")
)

left, right = st.columns(2)

with left:

    fig = px.line(
        df,
        x="timestamp",
        y="market_cap",
        title="Market Cap Trend",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.line(
        df,
        x="timestamp",
        y="volume_24h",
        title="24H Volume Trend",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )