import pandas as pd

df = pd.read_csv("data/live_prices.csv", skiprows=5, header=0)
df.columns = ["mandi", "arrivals", "unit", "crop", "min_price", "max_price", "modal_price", "price_unit"]

df = df.dropna(subset=["mandi", "crop", "modal_price"])
df = df[df["mandi"].str.contains("APMC", na=False)]

df["mandi"] = df["mandi"].str.replace(" APMC", "").str.strip()
df["modal_price"] = pd.to_numeric(df["modal_price"], errors="coerce")
df["crop"] = df["crop"].str.strip()

df_clean = df[["mandi", "crop", "modal_price"]].rename(columns={"modal_price": "price"})
df_clean["district"] = df_clean["mandi"]
df_clean["state"] = "Madhya Pradesh"

df_clean.to_csv("data/real_prices.csv", index=False)
print(f"Clean data saved! Total records: {len(df_clean)}")
print(df_clean.head(10))