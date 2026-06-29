import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Crypto Intelligence Platform",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>



/* Hide footer */
footer {visibility: hidden;}



</style>
""", unsafe_allow_html=True)
ASSETS_DIR = Path(__file__).parent / "assets"

st.image(
    ASSETS_DIR / "logo.png",
    width=120
)

pg = st.navigation(
    [
        st.Page(
            "pages/1_🏠_Executive_Dashboard.py",
            title="Executive Dashboard",
            icon="🏠",
            default=True,
        ),
        st.Page(
            "pages/2_🪙_Coin_Explorer.py",
            title="Coin Explorer",
            icon="🪙",
        ),
        st.Page(
            "pages/3_📈_Market_Trends.py",
            title="Market Trends",
            icon="📈",
        ),
        st.Page(
            "pages/4_🏆_Market_Leaders.py",
            title="Market Leaders",
            icon="🏆",
        ),
        st.Page(
            "pages/5_⚙️_Pipeline_Status.py",
            title="Pipeline Status",
            icon="⚙️",
        ),
        st.Page(
            "pages/6_ℹ️_About_Project.py",
            title="About Project",
            icon="ℹ️",
        ),
    ]
)

pg.run()