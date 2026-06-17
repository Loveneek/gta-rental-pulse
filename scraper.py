from sample_data import sample_listings

def fetch_rentals():
    print(f"Fetched {len(sample_listings)} listings.")
    return sample_listings

def parse_listing(raw):
    return {
        "listing_id": raw["zpid"],
        "address":    raw["address"],
        "price":      raw["price"],
        "bedrooms":   raw["bedrooms"],
        "bathrooms":  raw["bathrooms"],
        "sqft":       raw["livingArea"]
    }