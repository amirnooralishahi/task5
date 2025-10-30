from decimal import Decimal
from typing import List

from pydantic import BaseModel



class ShowPostVendor(BaseModel):

    price_delivery: List[Decimal]|Decimal
    parcel_id : List[int]|int
    name_customer : List[str]|str
    lastName_customer : List[str]|str
    statusDelivery : List[str]|str

