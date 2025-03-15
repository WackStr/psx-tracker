from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models.share_price import share_price

app = FastAPI()

@app.get("/share-price/{script}")
async def get_share_price(script: str, db: Session  = Depends(get_db)):
    """get_price_of_share"""
    return db.query(share_price).all()