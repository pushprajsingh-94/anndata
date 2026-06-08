import numpy as np
from datetime import datetime, timedelta

def predict_prices(crop, mandi, days=14):
    prices_map = {
        "Wheat": 2340, "Chana": 4350, "Soya": 3900, "Makka": 1800
    }
    
    base_price = prices_map.get(crop, 2000)
    
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