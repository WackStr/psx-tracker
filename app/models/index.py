from sqlalchemy import Column, Integer, String, TIMESTAMP
from ..database import Base

class index(Base):
    
    __tablename__ = "t_index"
    
    id = Column(Integer, primary_key = True, index=True)
    index_name = Column(String)
    created_on = Column(TIMESTAMP)