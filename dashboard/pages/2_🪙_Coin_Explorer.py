import streamlit as st

from charts import price_history_chart
from utils import load_coin_history

st.set_page_config(
    page_title="Coin Explorer",
    page_icon="🪙",
    layout="wide"
)

st.title("🪙 Coin Explorer")

coin_history = load_coin_history()

coins = sorted(
    coin_history["coin"].unique()
)

selected_coin = st.selectbox(
    "Select Coin",
    coins
)

coin_df = (
    coin_history[
        coin_history["coin"] == selected_coin
    ]
    .sort_values("timestamp")
)

st.subheader(f"{selected_coin.title()} Price History")

fig = price_history_chart(
    coin_df
)

st.plotly_chart(
    fig,
    use_container_width=True
)