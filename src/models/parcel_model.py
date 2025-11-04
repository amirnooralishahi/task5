from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING, Any, List, Dict
from models.model_abstract import ModelAbstract




class ParcelModel(ModelAbstract):
    def repository(self) -> Any:
        from repository.parcelRepo import RepositoryParcel
        return  RepositoryParcel
    id : int
    vendor_id : int
    customer_id : int
    price : Decimal
    share_company:Decimal
    invoice_id : int
    updated_at : datetime
    created_at : datetime
    status: str
    origin:str | None
    def invoice (self):
        return self.relation('invoice')


    def vendor(self):
        return  self.relation('vendor')

    def customer(self):
        return self.relation('customer')

    def invoice(self):
        return self.relation('invoice')




