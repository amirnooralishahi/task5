from decimal import Decimal
from typing import Optional

from pydantic import BaseModel ,constr





class CreateVendorSchema(BaseModel):
    name: str
    last_name: str
    phone: constr(max_length=11)
    national_code: int
    balance : Optional[Decimal]
    city :Optional[str]

class ShowVendorSchema(BaseModel):

    id : int
    name : str
    last_name : str
    phone : int
    balance : Decimal




