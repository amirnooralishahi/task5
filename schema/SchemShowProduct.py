from typing import Optional, List

from pydantic import BaseModel
from decimal import Decimal

class ShowProductSchema(BaseModel):
    name_vendor:List[str]|str
    last_name_vendor: List[str]|str
    price:List[Decimal]|Decimal
    name : List[str]|str
    count: Optional[int]=1
