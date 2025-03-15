from sqlalchemy import Column, Integer, String, TIMESTAMP, DECIMAL
from ..database import Base

class share_price(Base):
    
    __tablename__ = "t_share_price"
    
    id = Column(Integer, primary_key =True, index=True)
    company_script = Column(String)
    measured_on = Column(TIMESTAMP)
    price = Column(DECIMAL)