import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="GTA Rental Pulse", page_icon="🏠", layout="wide")

@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM listings", conn)
    conn.close()
    return df

df = load_data()

st.title("🏠 GTA Rental Pulse")
st.write("Toronto rental market trends across 12 neighbourhoods")

st.divider()

# Top metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Listings", f"{len(df):,}")
col2.metric("Avg Rent", f"${int(df['price'].mean()):,}")
col3.metric("Avg Sqft", f"{int(df['sqft'].mean()):,}")
col4.metric("Neighbourhoods", df['neighbourhood'].nunique())

st.divider()

# Most and least expensive
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔴 Most Expensive Areas")
    top = df.groupby("neighbourhood")["price"].mean().sort_values(ascending=False).head(5)
    st.bar_chart(top)

with col2:
    st.subheader("🟢 Most Affordable Areas")
    bottom = df.groupby("neighbourhood")["price"].mean().sort_values(ascending=True).head(5)
    st.bar_chart(bottom)

st.divider()

st.subheader("📋 Recent Listings")
st.dataframe(
    df[["address", "neighbourhood", "price", "bedrooms", "sqft"]]
    .sort_values("price", ascending=False)
    .head(10),
    use_container_width=True
)