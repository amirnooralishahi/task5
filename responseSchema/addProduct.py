from datetime import datetime
from pydantic import BaseModel ,condecimal




class ResponseAddProduct(BaseModel):
    vendor_id:int
    name:str
    count:int
    price:condecimal(max_digits=10, decimal_places=2)
    created_at: datetime




