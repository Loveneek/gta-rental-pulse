from scraper import fetch_rentals, parse_listing
from database import insert_listing

def run():
    print("=== GTA Rental Pulse ===")
    
    raw_listings = fetch_rentals()
    
    saved = 0
    for raw in raw_listings:
        listing = parse_listing(raw)
        insert_listing(listing)
        saved += 1
    
    print(f"Done. {saved} listings saved to database.")

run()