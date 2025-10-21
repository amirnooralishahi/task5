from decimal import Decimal

from pydantic import BaseModel



class ShowParcel(BaseModel):
    id:int
    TotalPrice : int
    price: int
    nameProduct : str
    count : int
    status:str
    origin: str

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

