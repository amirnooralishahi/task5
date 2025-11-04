import decimal

from pydantic import BaseModel






class AddProductItem(BaseModel):
    name_product : str
    count : int
    price : decimal.Decimal
    vendor_id : int
