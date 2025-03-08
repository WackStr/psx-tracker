from pydantic import BaseModel

class company(BaseModel):
    market_cap: float
    shares: int
    free_float: int
    free_float_percentage: float