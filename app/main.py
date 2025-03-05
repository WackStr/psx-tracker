from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Company(BaseModel):
    category: str
    company_name: str
    script: str
    
class CompanyMeasurement(BaseModel):
    market_cap: float
    shares: int
    free_float: int
    free_float_percentage: float
    
class IndexSegment(BaseModel):
    company: Company
    percentage: float
    
class SharePrice(BaseModel):
    company: Company
    price: float
    timestamp: datetime
    

@app.get("/share-price/{script}")
async def get_share_price(script: str):
    """get_price_of_share"""
    return {"share-price": 10.0}