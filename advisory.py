import pandas as pd
import os

DATA = [
    {"mandi": "Indore", "crop": "Wheat", "price": 2340, "district": "Indore"},
    {"mandi": "Hoshangabad", "crop": "Wheat", "price": 2100, "district": "Hoshangabad"},
    {"mandi": "Itarsi", "crop": "Wheat", "price": 2180, "district": "Hoshangabad"},
    {"mandi": "Bhopal", "crop": "Wheat", "price": 2220, "district": "Bhopal"},
    {"mandi": "Narsinghpur", "crop": "Wheat", "price": 2200, "district": "Narsinghpur"},
    {"mandi": "Sehore", "crop": "Wheat", "price": 2310, "district": "Sehore"},
    {"mandi": "Indore", "crop": "Chana", "price": 4350, "district": "Indore"},
    {"mandi": "Hoshangabad", "crop": "Chana", "price": 4000, "district": "Hoshangabad"},
    {"mandi": "Bhopal", "crop": "Chana", "price": 4200, "district": "Bhopal"},
    {"mandi": "Sehore", "crop": "Chana", "price": 4300, "district": "Sehore"},
    {"mandi": "Indore", "crop": "Soya", "price": 3900, "district": "Indore"},
    {"mandi": "Hoshangabad", "crop": "Soya", "price": 3600, "district": "Hoshangabad"},
    {"mandi": "Bhopal", "crop": "Soya", "price": 3700, "district": "Bhopal"},
    {"mandi": "Narsinghpur", "crop": "Soya", "price": 3550, "district": "Narsinghpur"},
    {"mandi": "Indore", "crop": "Makka", "price": 1800, "district": "Indore"},
    {"mandi": "Hoshangabad", "crop": "Makka", "price": 1650, "district": "Hoshangabad"},
    {"mandi": "Bhopal", "crop": "Makka", "price": 1700, "district": "Bhopal"},
]

def get_advisory(crop, district):
    df = pd.DataFrame(DATA)
    crop_data = df[df["crop"] == crop]
    best_mandi = crop_data.loc[crop_data["price"].idxmax()]
    
    your_data = crop_data[crop_data["district"] == district]
    if len(your_data) > 0:
        your_price = int(your_data["price"].mean())
        your_mandi = district
    else:
        your_price = int(crop_data["price"].min())
        your_mandi = str(crop_data.loc[crop_data["price"].idxmin()]["mandi"])
    
    profit_per_quintal = int(best_mandi["price"]) - your_price
    extra_earning = profit_per_quintal * 10
    
    advisory = {
        "crop": crop,
        "best_mandi": str(best_mandi["mandi"]),
        "best_price": int(best_mandi["price"]),
        "your_mandi": your_mandi,
        "your_price": your_price,
        "profit_per_quintal": profit_per_quintal,
        "extra_earning_10_quintal": extra_earning,
        "message": f"Go to {best_mandi['mandi']} mandi — earn Rs.{profit_per_quintal} more per quintal!"
    }
    return advisory