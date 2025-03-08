from pydantic import BaseModel

class company(BaseModel):
    category: str
    company_name: str
    script: str