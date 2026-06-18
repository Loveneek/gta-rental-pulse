# 🏠 GTA Rental Pulse

> A full-stack data pipeline that collects, stores, and analyzes Toronto rental market listings — built with Python, PostgreSQL, and Streamlit.

🔗 **[Live Dashboard → gta-rental-pulse.streamlit.app](https://gta-rental-pulse.streamlit.app)**  
📁 **[GitHub Repository](https://github.com/Loveneek/gta-rental-pulse)**

---

## 📌 Project Overview

GTA Rental Pulse is an end-to-end data engineering project that simulates a real rental market analytics platform for the Greater Toronto Area. It covers the full data pipeline lifecycle:

**Collect → Store → Analyze → Visualize → Deploy**

The dashboard tracks rental trends across 12 GTA neighbourhoods, providing insights on average rent by area, pricing per square foot, bedroom type distributions, and affordability comparisons — all powered by a live cloud database.

---

## 🚀 Live Features

- **4-page interactive dashboard** with sidebar navigation
- **Market Overview** — total listings, average rent, average sqft, neighbourhood count
- **Neighbourhood Analysis** — filter by area, compare average rents and price/sqft across all neighbourhoods
- **Bedroom Breakdown** — rent by bedroom type, listing distribution, best value listings by sqft/dollar
- **Price Analysis** — min/max/median rent, price range table by neighbourhood, most expensive and most affordable listings

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.13 |
| Database | PostgreSQL (Supabase cloud) |
| Dashboard | Streamlit |
| Data Manipulation | Pandas |
| DB Connector | psycopg2 |
| Data Generation | Faker |
| Deployment | Streamlit Cloud |
| Version Control | Git + GitHub |

---

## 🏗️ Architecture

```
generate_data.py
      │
      ▼
  scraper.py  ──►  parse_listing()
      │
      ▼
  database.py ──►  PostgreSQL (Supabase)
      │
      ▼
  dashboard.py + pages/
      │
      ▼
  Streamlit Cloud (Live URL)
```

**Data Flow:**
1. `generate_data.py` generates realistic GTA rental listings using the Faker library, modeled on real 2026 GTA market price ranges per neighbourhood
2. `scraper.py` parses and structures raw listing data into clean dictionaries
3. `database.py` connects to Supabase PostgreSQL and handles all inserts with duplicate prevention via `ON CONFLICT DO NOTHING`
4. `dashboard.py` and the `pages/` folder pull live data from the cloud DB and render interactive charts and tables via Streamlit

---

## 📁 Project Structure

```
gta-rental-pulse/
├── dashboard.py          # Home page — market overview
├── pages/
│   ├── 1_Neighbourhood.py    # Neighbourhood comparison analysis
│   ├── 2_Bedrooms.py         # Bedroom type breakdown
│   └── 3_Price_Analysis.py   # Price per sqft, ranges, top/bottom listings
├── database.py           # PostgreSQL connection, table creation, insert logic
├── scraper.py            # Data parsing layer
├── generate_data.py      # Realistic GTA rental data generator (200+ listings)
├── main.py               # Pipeline runner — ties scraper + database together
├── sample_data.py        # Static sample dataset for local testing
├── requirements.txt      # Python dependencies
└── .env                  # Local environment variables (not committed)
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE listings (
    id            SERIAL PRIMARY KEY,
    listing_id    VARCHAR(50) UNIQUE,
    address       TEXT,
    neighbourhood VARCHAR(100),
    price         INTEGER,
    bedrooms      INTEGER,
    bathrooms     NUMERIC(3,1),
    sqft          INTEGER,
    date_scraped  DATE DEFAULT CURRENT_DATE
);
```

Key design decisions:
- `UNIQUE` on `listing_id` prevents duplicate entries
- `ON CONFLICT DO NOTHING` makes the pipeline safely re-runnable
- `DEFAULT CURRENT_DATE` on `date_scraped` auto-timestamps every ingestion run

---

## 📊 Key SQL Queries Used

**Average rent by neighbourhood:**
```sql
SELECT neighbourhood, AVG(price)
FROM listings
GROUP BY neighbourhood
ORDER BY AVG(price) DESC;
```

**Price per sqft analysis:**
```sql
SELECT neighbourhood, AVG(price::float / sqft) AS price_per_sqft
FROM listings
GROUP BY neighbourhood
ORDER BY price_per_sqft DESC;
```

**Most affordable listings:**
```sql
SELECT address, neighbourhood, price, bedrooms, sqft
FROM listings
ORDER BY price ASC
LIMIT 10;
```

---

## 🏘️ Neighbourhoods Covered

| Neighbourhood | Price Range |
|--------------|-------------|
| Yorkville | $3,200 – $6,000 |
| Downtown Core | $2,800 – $5,000 |
| King West | $2,600 – $4,500 |
| Queen West | $2,200 – $3,800 |
| Vaughan | $1,900 – $3,100 |
| Mississauga | $1,800 – $3,200 |
| Leslieville | $1,900 – $3,200 |
| North York | $1,800 – $3,000 |
| Markham | $1,800 – $3,000 |
| Etobicoke | $1,700 – $2,900 |
| Scarborough | $1,600 – $2,800 |
| Brampton | $1,600 – $2,600 |

---

## ⚙️ How to Run Locally

**1. Clone the repo:**
```bash
git clone https://github.com/Loveneek/gta-rental-pulse
cd gta-rental-pulse
```

**2. Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables:**

Create a `.env` file in the project root:
```
DATABASE_URL=your_postgresql_connection_string
```

**5. Initialize database and load data:**
```bash
python -c "from database import create_table; create_table()"
python generate_data.py
```

**6. Run the dashboard:**
```bash
streamlit run dashboard.py
```

---

## 🌐 Deployment

The app is deployed on **Streamlit Cloud** connected to a **Supabase PostgreSQL** cloud database.

- Streamlit Cloud reads the `DATABASE_URL` from its Secrets manager (equivalent to `.env` for production)
- Any push to the `main` branch on GitHub triggers an automatic redeploy
- The database persists independently of the app — data survives redeployments

---

## 📈 Sample Insights

- Average GTA rent across all listings: **~$3,182/month**
- **Yorkville** is the most expensive neighbourhood, averaging $4,500+
- **Brampton** and **Scarborough** offer the most affordable options under $2,000
- 3-bedroom units cost approximately **40% more** than 1-bedroom units on average
- Downtown Core has the highest **price per sqft**, while Etobicoke offers the best sqft per dollar

---

## 🔮 Future Improvements

- Integrate a live Canadian rental API (CMHC open data) for real listing ingestion
- Add Selenium-based scraper for torontorentals.com dynamic listings
- Schedule daily pipeline runs using GitHub Actions or cron
- Add date-range filtering to track price trends over time
- Email alerts when average rent in a neighbourhood changes by more than 5%

---

## 👨‍💻 Author

**Loveneek Singh**  
Software Engineering Student — York University (2027)  
📧 singhloveneek8@gmail.com  
🔗 [GitHub](https://github.com/Loveneek)

---

*Built as a portfolio project to demonstrate end-to-end data pipeline engineering using Python, PostgreSQL, and cloud deployment.*