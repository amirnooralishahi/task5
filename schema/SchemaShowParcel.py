from decimal import Decimal

from pydantic import BaseModel



class ShowParcel(BaseModel):
    TotalPrice : Decimal
    price: Decimal
    nameProduct : str
    count : int
    status:str