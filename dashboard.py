import streamlit as st
import pandas as pd
from database import get_connection

st.title("GTA Rental Pulse")
st.write("Toronto rental market trends")

# Pull data from database FIRST
conn = get_connection()
df = pd.read_sql("SELECT * FROM listings", conn)
conn.close()

# Sidebar filter AFTER df exists
st.sidebar.header("Filters")
neighbourhoods = ["All"] + sorted(df["neighbourhood"].unique().tolist())
selected = st.sidebar.selectbox("Neighbourhood", neighbourhoods)

# Apply filter
if selected != "All":
    df = df[df["neighbourhood"] == selected]

# Summary stats
st.subheader("Market Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Listings", len(df))
col2.metric("Avg Rent", f"${int(df['price'].mean())}")
col3.metric("Avg Sqft", f"{int(df['sqft'].mean())}")

# Table of all listings
st.subheader("All Listings")
st.dataframe(df)

# Average rent by bedrooms
st.subheader("Average Rent by Bedrooms")
avg_by_bed = df.groupby("bedrooms")["price"].mean().reset_index()
avg_by_bed.columns = ["Bedrooms", "Average Rent"]
st.bar_chart(avg_by_bed.set_index("Bedrooms"))

# Most expensive listings
st.subheader("Top 5 Most Expensive Listings")
top5 = df.sort_values("price", ascending=False).head(5)
st.dataframe(top5[["address", "price", "bedrooms", "sqft"]])