from fastapi import FastAPI
from advisory import get_advisory

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AnnData API chal rahi hai!"}

@app.get("/advisory")
def advisory(crop: str, district: str):
    result = get_advisory(crop, district)
    return result