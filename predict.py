import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def predict_prices(crop, mandi, days=14):
    df = pd.read_csv("data/real_prices.csv")
    
    crop_mandi_data = df[(df["crop"] == crop) & (df["mandi"] == mandi)]
    
    if len(crop_mandi_data) == 0:
        return None
    
    base_price = int(crop_mandi_data["price"].mean())
    
    dates = []
    prices = []
    
    for i in range(days):
        date = datetime.today() + timedelta(days=i)
        dates.append(date.strftime("%d %b"))
        
        trend = i * 8
        seasonal = 50 * np.sin(i * 0.5)
        noise = np.random.randint(-30, 30)
        
        predicted_price = base_price + trend + seasonal + noise
        prices.append(int(predicted_price))
    
    return {"dates": dates, "prices": prices, "base_price": base_price}