import pandas as pd
import streamlit as st
import pyarrow.dataset as ds
import s3fs

BUCKET = "om-crypto-intelligence-dev"

# Local development (AWS CLI profile)
if not hasattr(st, "secrets") or "AWS_ACCESS_KEY_ID" not in st.secrets:
    fs = s3fs.S3FileSystem(
        profile="crypto-project"
    )

# Streamlit Cloud deployment
else:
    fs = s3fs.S3FileSystem(
        key=st.secrets["AWS_ACCESS_KEY_ID"],
        secret=st.secrets["AWS_SECRET_ACCESS_KEY"],
        client_kwargs={
            "region_name": st.secrets["AWS_DEFAULT_REGION"]
        }
    )


@st.cache_data
def load_parquet(path):

    dataset = ds.dataset(
        f"{BUCKET}/{path}",
        filesystem=fs,
        format="parquet",
        partitioning="hive"
    )

    return dataset.to_table().to_pandas()


@st.cache_data
def load_coin_history():

    return load_parquet(
        "gold/coin_history/"
    )


@st.cache_data
def load_market_summary():

    return load_parquet(
        "gold/market_summary/"
    )


@st.cache_data
def load_top_market_cap():

    return load_parquet(
        "gold/top_market_cap/"
    )


@st.cache_data
def load_top_gainers():

    return load_parquet(
        "gold/top_gainers/"
    )


@st.cache_data
def load_top_losers():

    return load_parquet(
        "gold/top_losers/"
    )


@st.cache_data
def load_highest_volume():

    return load_parquet(
        "gold/highest_volume/"
    )


def format_number(num):

    if num >= 1_000_000_000_000:
        return f"${num/1_000_000_000_000:.2f}T"

    elif num >= 1_000_000_000:
        return f"${num/1_000_000_000:.2f}B"

    elif num >= 1_000_000:
        return f"${num/1_000_000:.2f}M"

    elif num >= 1_000:
        return f"${num/1_000:.2f}K"

    else:
        return f"${num:.2f}"