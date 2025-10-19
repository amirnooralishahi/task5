from typing import Optional

from pydantic import BaseModel
from decimal import Decimal

class ShowProductSchema(BaseModel):
    name_vendor:str
    last_name_vendor: str
    price:Decimal
    name : str
    count: Optional[int]=1
