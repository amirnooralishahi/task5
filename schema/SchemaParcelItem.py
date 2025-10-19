import datetime
from typing import Optional, List

from pydantic import BaseModel,Json
from decimal import Decimal


class ParcelItemSchema(BaseModel):
    name:str

    class Config:
        from_attributes = True

class CreateParcelItemSchema(BaseModel):

    parcel_id : int
    product_id : int
    price: Decimal
    count: int


