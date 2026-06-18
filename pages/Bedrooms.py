import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="Bedroom Analysis", page_icon="🛏️", layout="wide")

@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM listings", conn)
    conn.close()
    return df

df = load_data()

st.title("🛏️ Bedroom Breakdown")
st.divider()

# Metrics per bedroom type
st.subheader("Average Rent by Bedroom Count")
avg_by_bed = df.groupby("bedrooms")["price"].mean().sort_index()
st.bar_chart(avg_by_bed)

st.divider()

# Listing count by bedrooms
st.subheader("Number of Listings by Bedroom Count")
count_by_bed = df.groupby("bedrooms")["price"].count()
count_by_bed.index = count_by_bed.index.map({0: "Studio", 1: "1 Bed", 2: "2 Bed", 3: "3 Bed"})
st.bar_chart(count_by_bed)

st.divider()

# Average sqft by bedrooms
st.subheader("Average Sqft by Bedroom Count")
sqft_by_bed = df.groupby("bedrooms")["sqft"].mean().sort_index()
st.bar_chart(sqft_by_bed)

st.divider()

# Best value listings — highest sqft per dollar
st.subheader("🏆 Best Value Listings (Most Sqft per Dollar)")
df["sqft_per_dollar"] = (df["sqft"] / df["price"]).round(4)
best_value = df.sort_values("sqft_per_dollar", ascending=False).head(10)
st.dataframe(
    best_value[["address", "neighbourhood", "price", "bedrooms", "sqft", "sqft_per_dollar"]],
    use_container_width=True
)