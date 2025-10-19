from decimal import Decimal

from pydantic import BaseModel



class ShowParcel(BaseModel):
    id: int
    TotalPrice : Decimal
    price: Decimal
    nameProduct : str
    count : int
    status:str