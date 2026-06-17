import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="rental_pulse",
        user="loveneekgill",
        password=""
    )

def test_connection():
    conn = get_connection()
    print("Connected successfully!")
    conn.close()

def insert_listing(data):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO listings 
            (listing_id, address, price, bedrooms, bathrooms, sqft)
        VALUES 
            (%s, %s, %s, %s, %s, %s)
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
    print(f"Inserted: {data['address']}")

test_listing = {
    "listing_id": "1001",
    "address": "210 Victoria St, Toronto",
    "price": 2400,
    "bedrooms": 1,
    "bathrooms": 1.0,
    "sqft": 650
}

insert_listing(test_listing)