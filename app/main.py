from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


from .database import get_db
from .models.share_price import share_price

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/share-price/{script}")
async def get_share_price(script: str, db: Session  = Depends(get_db)):
    """get_price_of_share"""
    return db.query(share_price).filter(share_price.company_script == script).all()