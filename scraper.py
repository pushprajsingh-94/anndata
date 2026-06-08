import requests
import pandas as pd
from datetime import datetime, timedelta
import os

def fetch_agmarknet_data():
    print("Fetching data...")
    
    yesterday = datetime.today() - timedelta(days=2)
    date_str = yesterday.strftime("%d-%b-%Y")
    
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    
    url = f"https://agmarknet.gov.in/PriceAndArrivals/CommodityDailyStateWiseExport.aspx?date={date_str}&statecode=23&commodity=0&district=0&market=0&language=E&filetype=csv"
    
    try:
        response = session.get(url, timeout=30)
        print("Status:", response.status_code)
        print("Content type:", response.headers.get("content-type"))
        print("Content preview:", response.text[:300])
        
        if response.status_code == 200:
            with open("data/real_prices.csv", "wb") as f:
                f.write(response.content)
            print("Data saved!")
            
    except Exception as e:
        print(f"Error: {e}")

fetch_agmarknet_data()