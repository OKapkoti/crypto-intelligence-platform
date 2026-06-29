import streamlit as st
from charts import (
    price_history_chart,
    trend_chart
)
from utils import (
    load_coin_history,
    load_market_summary,
    load_top_market_cap,
    load_top_gainers,
    load_top_losers,
    load_highest_volume,
    format_number
)

st.set_page_config(
    page_title="CryptoPulse",
    page_icon="📊",
    layout="wide"
)


# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------

market_summary = load_market_summary()
coin_history = load_coin_history()
top_market_cap = load_top_market_cap()
highest_volume = load_highest_volume()
top_gainers = load_top_gainers()
top_losers = load_top_losers()


# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

st.sidebar.header("📌 Filters")

dates = sorted(
    coin_history["snapshot_date"].unique(),
    reverse=True
)

selected_date = st.sidebar.selectbox(
    "Date",
    dates
)

filtered = coin_history[
    coin_history["snapshot_date"] == selected_date
]

hours = sorted(
    filtered["snapshot_hour"].unique()
)

selected_hour = st.sidebar.selectbox(
    "Hour",
    hours
)

filtered = filtered[
    filtered["snapshot_hour"] == selected_hour
]

# -----------------------------------------------------
# HEADER
# -----------------------------------------------------

latest = (
    market_summary
    .sort_values(
        "snapshot_time",
        ascending=False
    )
    .iloc[0]
)

header_left, header_right = st.columns([4,1])

with header_left:

    st.title("CryptoPulse")

    st.caption("Real-Time Cryptocurrency Analytics Platform")
with header_right:

    st.metric(
        "🕒 Last Updated",
        latest["snapshot_time"].strftime("%d %b %Y, %I:%M %p")
    )

st.markdown("---")



col1, col2, col3, col4 = st.columns(4)

cards = [
    ("🪙", "Total Coins", latest["total_coins"]),
    ("💰", "Market Cap", format_number(latest["total_market_cap"])),
    ("📊", "24H Volume", format_number(latest["total_volume_24h"])),
    ("💵", "Average Price", format_number(latest["average_price"]))
]

for col, card in zip([col1, col2, col3, col4], cards):

    icon, title, value = card

    with col:

        st.markdown(
            f"""
<div style="
background:#1E1E1E;
padding:18px;
border-radius:15px;
border:1px solid #333;
text-align:center;
">

<div style="font-size:32px;">{icon}</div>

<div style="font-size:18px;
font-weight:bold;
margin-top:8px;">
{title}
</div>

<div style="
font-size:30px;
color:#00D4AA;
margin-top:10px;
font-weight:bold;">
{value}
</div>

</div>
""",
            unsafe_allow_html=True
        )
st.markdown("---")

# -----------------------------------------------------
# FILTER GOLD TABLES
# -----------------------------------------------------

btc = (
    coin_history[
        coin_history["coin"] == "bitcoin"
    ]
    .sort_values("timestamp")
)

market_cap_filtered = top_market_cap[
    (top_market_cap["snapshot_date"] == selected_date)
    &
    (top_market_cap["snapshot_hour"] == selected_hour)
]

volume_filtered = highest_volume[
    (highest_volume["snapshot_date"] == selected_date)
    &
    (highest_volume["snapshot_hour"] == selected_hour)
]

gainers_filtered = top_gainers[
    (top_gainers["snapshot_date"] == selected_date)
    &
    (top_gainers["snapshot_hour"] == selected_hour)
]

losers_filtered = top_losers[
    (top_losers["snapshot_date"] == selected_date)
    &
    (top_losers["snapshot_hour"] == selected_hour)
]

# -----------------------------------------------------
# ROW 1
# -----------------------------------------------------



st.subheader("📈 Bitcoin Price History")

st.plotly_chart(
     price_history_chart(btc),
    use_container_width=True
)

st.markdown("---")

left, right = st.columns(2)

with left:

    st.subheader("📊 Market Cap Trend")

    st.plotly_chart(
        trend_chart(
            btc,
            x="timestamp",
            y="market_cap",
            title=""
        ),
        use_container_width=True
    )

with right:

    st.subheader("📊 24H Volume Trend")

    st.plotly_chart(
        trend_chart(
            btc,
            x="timestamp",
            y="volume_24h",
            title=""
        ),
        use_container_width=True
    )

# -----------------------------------------------------
# ROW 2
# -----------------------------------------------------


# -----------------------------------------------------
# ROW 3
# -----------------------------------------------------




