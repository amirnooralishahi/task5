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

    vendor_id: List[int]|int
    customer_id: int
    price: int
    count:int
    share_company:Optional[int]
    invoice_id : List[int]|int
    created_at:datetime.datetime
    origin:str
    status : str
    delivery:str
    methodpost:str
    class Config:
        from_attributes = True



