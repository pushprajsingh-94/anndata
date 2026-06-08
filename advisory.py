import pandas as pd

def get_advisory(crop, district):
    df = pd.read_csv("data/real_prices.csv")
    
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