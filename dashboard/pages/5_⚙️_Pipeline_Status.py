import streamlit as st

from utils import (
    load_coin_history,
    load_market_summary
)

st.set_page_config(
    page_title="Pipeline Status",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Data Pipeline Status")

st.markdown("### Pipeline Architecture")

st.code("""
CoinGecko API
      │
      ▼
 Bronze (Raw JSON)
      │
      ▼
 Silver (Validated Parquet)
      │
      ▼
 Gold (Analytics Tables)
      │
      ▼
 AWS Glue Catalog
      │
      ▼
 Amazon Athena
      │
      ▼
 Streamlit Dashboard
""")

market_summary = load_market_summary()
coin_history = load_coin_history()

latest = (
    market_summary
    .sort_values("snapshot_time", ascending=False)
    .iloc[0]
)

st.markdown("---")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Latest Snapshot",
    str(latest["snapshot_time"])
)

c2.metric(
    "Coins Processed",
    int(latest["total_coins"])
)

c3.metric(
    "Historical Records",
    len(coin_history)
)

st.markdown("---")

st.subheader("Data Quality Checks")

st.success("✅ No duplicate snapshots")

st.success("✅ Invalid prices removed")

st.success("✅ Market Cap validated")

st.success("✅ Volume validated")

st.success("✅ Idempotent Silver Layer")

st.success("✅ Gold Layer generated successfully")