import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="Price Analysis", page_icon="💰", layout="wide")

@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM listings", conn)
    conn.close()
    return df

df = load_data()

st.title("💰 Price Analysis")
st.divider()

# Price per sqft
df["price_per_sqft"] = (df["price"] / df["sqft"]).round(2)

# Overall price stats
col1, col2, col3, col4 = st.columns(4)
col1.metric("Lowest Rent", f"${int(df['price'].min()):,}")
col2.metric("Highest Rent", f"${int(df['price'].max()):,}")
col3.metric("Median Rent", f"${int(df['price'].median()):,}")
col4.metric("Avg Price/Sqft", f"${df['price_per_sqft'].mean():.2f}")

st.divider()

# Price distribution by neighbourhood and bedroom
st.subheader("Price Range by Neighbourhood")
price_range = df.groupby("neighbourhood").agg(
    Min=("price", "min"),
    Average=("price", "mean"),
    Max=("price", "max")
).round(0).astype(int).sort_values("Average", ascending=False)
st.dataframe(price_range, use_container_width=True)

st.divider()

# Most expensive listings
st.subheader("🔴 Top 10 Most Expensive Listings")
top10 = df.sort_values("price", ascending=False).head(10)
st.dataframe(
    top10[["address", "neighbourhood", "price", "bedrooms", "sqft", "price_per_sqft"]],
    use_container_width=True
)

st.divider()

# Most affordable listings
st.subheader("🟢 Top 10 Most Affordable Listings")
bottom10 = df.sort_values("price", ascending=True).head(10)
st.dataframe(
    bottom10[["address", "neighbourhood", "price", "bedrooms", "sqft", "price_per_sqft"]],
    use_container_width=True
)

st.divider()

# Best price per sqft
st.subheader("📐 Best Price per Sqft by Neighbourhood")
best_sqft = df.groupby("neighbourhood")["price_per_sqft"].mean().sort_values(ascending=True)
st.bar_chart(best_sqft)