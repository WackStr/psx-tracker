from pydantic import BaseModel
import company

class index_segment(BaseModel):
    company: company
    percentage: float