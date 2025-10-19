import datetime
from typing import Optional, List

from pydantic import BaseModel,Json
from decimal import Decimal
from .SchemaParcelItem import ParcelItemSchema
from sqlalchemy.sql.sqltypes import TIMESTAMP


class CreateParcelSchema(BaseModel):
    vendor_name : str
    last_name_vendor : str
    invoice:int
    status : str
    count: int
    product_id: str
    customer_name:dict


class ProductParcelSchema(BaseModel):
    id: int
    vendor_id: int
    customer_id: int
    price: Decimal
    share_company:Optional[Decimal]
    invoice_id : int
    data:int
    origin:str
    status : str

    class Config:
        from_attributes = True



