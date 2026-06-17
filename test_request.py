import requests

response = requests.get("https://api.github.com")

# Convert the raw text into a Python dictionary
# data = response.json()

# print(type(data))                    # now it's a dict, not a string
# print(data["current_user_url"])      # access a specific value by key
# print(data.keys())                   # see all available keys

# print(data["totalResults"])
# print(data["results"][1]["address"])
# print(data["results"][0]["price"])
# print(data["results"][1]["details"]["sqft"])


# data = {
#     "totalResults": 2,
#     "results": [
#         {
#             "address": "123 King St, Toronto",
#             "price": 2500,
#             "bedrooms": 2,
#             "details": {
#                 "sqft": 900,
#                 "type": "Apartment"
#             }
#         },
#         {
#             "address": "456 Queen St, Toronto",
#             "price": 1800,
#             "bedrooms": 1,
#             "details": {
#                 "sqft": 600,
#                 "type": "Condo"
#             }
#         }
#     ]
# }

# # Your job — write code to print these four things:
# # 1. Total number of results
# # 2. Address of the second listing
# # 3. Price of the first listing
# # 4. sqft of the second listing
# for x in data["results"]:
#     address=x["address"]
#     cost=x["price"]
#     print(f"{address} - ${cost}")
    

from scraper import fetch_rentals, parse_listing

raw_listings = fetch_rentals()

for raw in raw_listings:
    listing = parse_listing(raw)
    print(f"{listing['address']} — ${listing['price']} — {listing['bedrooms']}bed")