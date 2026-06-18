import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="Neighbourhood Analysis", page_icon="🏘️", layout="wide")

@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM listings", conn)
    conn.close()
    return df

df = load_data()

st.title("🏘️ Neighbourhood Analysis")
st.divider()

# Filter
selected = st.selectbox("Select Neighbourhood", ["All"] + sorted(df["neighbourhood"].unique().tolist()))
if selected != "All":
    filtered = df[df["neighbourhood"] == selected]
else:
    filtered = df

# Metrics for selected neighbourhood
col1, col2, col3 = st.columns(3)
col1.metric("Listings", len(filtered))
col2.metric("Avg Rent", f"${int(filtered['price'].mean()):,}")
col3.metric("Avg Sqft", f"{int(filtered['sqft'].mean()):,}")

st.divider()

# Average rent by neighbourhood
st.subheader("Average Rent by Neighbourhood")
avg_rent = df.groupby("neighbourhood")["price"].mean().sort_values(ascending=False)
st.bar_chart(avg_rent)

st.divider()

# Price per sqft
st.subheader("Price per Sqft by Neighbourhood")
df["price_per_sqft"] = (df["price"] / df["sqft"]).round(2)
price_sqft = df.groupby("neighbourhood")["price_per_sqft"].mean().sort_values(ascending=False)
st.bar_chart(price_sqft)

st.divider()

# Raw data for selected neighbourhood
st.subheader(f"Listings — {selected}")
st.dataframe(
    filtered[["address", "price", "bedrooms", "bathrooms", "sqft"]]
    .sort_values("price", ascending=False),
    use_container_width=True
)