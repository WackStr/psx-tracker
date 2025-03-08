from pydantic import BaseModel
import company
from datetime import datetime

class share_price(BaseModel):
    company: company
    price: float
    timestamp: datetime