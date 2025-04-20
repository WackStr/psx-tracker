from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.share_price import share_price

from app.dependencies import get_current_user

router = APIRouter()

@router.get("/share-price/{script}")
async def get_share_price(script: str, db: Session  = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """get_price_of_share"""
    return db.query(share_price).filter(share_price.company_script == script).all()