import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id SERIAL PRIMARY KEY,
            listing_id VARCHAR(50) UNIQUE,
            address TEXT,
            price INTEGER,
            bedrooms INTEGER,
            bathrooms NUMERIC(3,1),
            sqft INTEGER,
            date_scraped DATE DEFAULT CURRENT_DATE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_listing(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO listings 
            (listing_id, address, price, bedrooms, bathrooms, sqft)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (listing_id) DO NOTHING;
    """, (
        data["listing_id"],
        data["address"],
        data["price"],
        data["bedrooms"],
        data["bathrooms"],
        data["sqft"]
    ))
    conn.commit()
    cur.close()
    conn.close()