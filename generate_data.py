import random
from faker import Faker

fake = Faker()

# Real Toronto neighbourhoods with realistic 2026 rent ranges
NEIGHBOURHOODS = {
    "Downtown Core":     (2800, 5000),
    "Yorkville":         (3200, 6000),
    "King West":         (2600, 4500),
    "Queen West":        (2200, 3800),
    "Leslieville":       (1900, 3200),
    "Scarborough":       (1600, 2800),
    "North York":        (1800, 3000),
    "Etobicoke":         (1700, 2900),
    "Mississauga":       (1800, 3200),
    "Brampton":          (1600, 2600),
    "Vaughan":           (1900, 3100),
    "Markham":           (1800, 3000),
}

def generate_listing(listing_id):
    # Pick a random neighbourhood
    neighbourhood = random.choice(list(NEIGHBOURHOODS.keys()))
    min_price, max_price = NEIGHBOURHOODS[neighbourhood]
    
    # Pick bedrooms — weighted toward 1 and 2 bed (most common in GTA)
    bedrooms = random.choices([0, 1, 2, 3], weights=[10, 35, 35, 20])[0]
    
    # Price goes up with bedrooms
    base_price = random.randint(min_price, max_price)
    price = base_price + (bedrooms * 200)
    
    # Sqft based on bedrooms
    sqft_ranges = {0: (380, 550), 1: (500, 750), 2: (700, 1050), 3: (950, 1400)}
    sqft = random.randint(*sqft_ranges[bedrooms])
    
    # Bathrooms based on bedrooms
    bathrooms = 1.0 if bedrooms <= 1 else (1.0 if bedrooms == 2 else 2.0)
    
    # Generate a fake street address
    address = f"{random.randint(1, 999)} {fake.street_name()}, {neighbourhood}"
    
    return {
        "listing_id": str(listing_id),
        "address": address,
        "neighbourhood": neighbourhood,
        "price": price,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "sqft": sqft
    }

# Generate 200 listings and print first 5 to verify
listings = [generate_listing(i) for i in range(1, 201)]
# for l in listings[:5]:
#     print(l)

# # Print to verify
# for neighbourhood, price_range in NEIGHBOURHOODS.items():
#     print(f"{neighbourhood}: ${price_range[0]} - ${price_range[1]}")

from database import insert_listing

def load_to_database():
    listings = [generate_listing(i) for i in range(1, 201)]
    saved = 0
    for listing in listings:
        insert_listing(listing)
        saved += 1
    print(f"Done. {saved} listings saved to database.")

load_to_database()