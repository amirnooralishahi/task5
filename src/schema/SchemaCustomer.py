from decimal import Decimal
from typing import Optional

from pydantic import BaseModel,constr




class CreateCustomerSchema(BaseModel):


    name : str
    last_name : str
    balance : Optional[Decimal]
    phone :constr(max_length=11)
    city: Optional[str]
    parcel_id: Optional[int]
    national_code : int


class ShowCustomerSchema(CreateCustomerSchema):
    id : int
    name:str
    last_name : str
    phone:constr(max_length=11)
    