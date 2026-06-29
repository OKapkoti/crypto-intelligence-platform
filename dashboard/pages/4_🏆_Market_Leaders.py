import streamlit as st

from charts import horizontal_bar

from utils import (
    load_top_market_cap,
    load_highest_volume,
    load_top_gainers,
    load_top_losers
)

st.set_page_config(
    page_title="Market Leaders",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Market Leaders")

top_market_cap = load_top_market_cap()
highest_volume = load_highest_volume()
top_gainers = load_top_gainers()
top_losers = load_top_losers()

latest_date = top_market_cap["snapshot_date"].max()

latest_hour = (
    top_market_cap[
        top_market_cap["snapshot_date"] == latest_date
    ]["snapshot_hour"].max()
)

market = top_market_cap[
    (top_market_cap["snapshot_date"] == latest_date)
    &
    (top_market_cap["snapshot_hour"] == latest_hour)
]

volume = highest_volume[
    (highest_volume["snapshot_date"] == latest_date)
    &
    (highest_volume["snapshot_hour"] == latest_hour)
]

gainers = top_gainers[
    (top_gainers["snapshot_date"] == latest_date)
    &
    (top_gainers["snapshot_hour"] == latest_hour)
]

losers = top_losers[
    (top_losers["snapshot_date"] == latest_date)
    &
    (top_losers["snapshot_hour"] == latest_hour)
]

left, right = st.columns(2)

with left:

    st.plotly_chart(
        horizontal_bar(
            market,
            "market_cap",
            "coin",
            "Top Market Cap"
        ),
        use_container_width=True
    )

with right:

    st.plotly_chart(
        horizontal_bar(
            volume,
            "volume_24h",
            "coin",
            "Highest Volume"
        ),
        use_container_width=True
    )

left, right = st.columns(2)

with left:

    st.plotly_chart(
        horizontal_bar(
            gainers,
            "change_24h",
            "coin",
            "Top Gainers"
        ),
        use_container_width=True
    )

with right:

    st.plotly_chart(
        horizontal_bar(
            losers,
            "change_24h",
            "coin",
            "Top Losers"
        ),
        use_container_width=True
    )