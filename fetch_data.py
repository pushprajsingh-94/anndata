import requests
import pandas as pd

API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

def fetch_live_prices():
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": "100",
        "filters[state]": "Madhya Pradesh"
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        print("Status:", response.status_code)
        data = response.json()
        records = data.get("records", [])
        print(f"Records fetched: {len(records)}")
        df = pd.DataFrame(records)
        print(df.head())
        df.to_csv("data/live_prices.csv", index=False)
        print("Live data saved!")
    except Exception as e:
        print("Error:", e)

fetch_live_prices()