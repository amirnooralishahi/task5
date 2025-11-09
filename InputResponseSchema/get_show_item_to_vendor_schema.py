from decimal import Decimal
from typing import List

from pydantic import BaseModel



class ShowParcel(BaseModel):
    id:List[int]|int
    TotalPrice : List[int]|int
    price: List[int]|int
    nameProduct :List[str]|str
    count : List[int]|int
    status:List[str]|str
    origin: List[str]|str=None

class ShowCancelParcel(BaseModel):
    TotalPrice: int
    price: int
    nameProduct: str
    count: int
    status: str
    origin: str
    sender:str

class ShowCancelInvoice(BaseModel):

    invoice_id: int
    customer_name: str
    status : str

