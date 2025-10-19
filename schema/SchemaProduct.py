from decimal import Decimal

from pydantic import BaseModel




class ProductSchema(BaseModel):
    id : int
    name : str
    vendor_id : int
    price: Decimal

    class Config:
        from_attributes = True
        