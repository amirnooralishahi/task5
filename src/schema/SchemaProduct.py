from decimal import Decimal
from numbers import Number
from typing import Optional

from pydantic import BaseModel




class addProduct(BaseModel):
    vendor_name : Optional[str]
    vendor_last_name:Optional[str]
    name_product : str
    price : Decimal
    count : Number

