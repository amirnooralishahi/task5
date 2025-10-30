from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING, Any, List, Dict
from models.model_abstract import ModelAbstract




class parcelItem(ModelAbstract):
    def repository(self) -> Any:
        from repository.parcelItem import  RepositoryItem
        return RepositoryItem

    id : int
    parcel_id : int
    price: int
    product_id: int
    count: int
    created_at: datetime
    updated_at: datetime
    share_company: Decimal

    def parcel(self)->int:
        return self.relation('parcel')

    def product(self)->int:
        return self.relation('product')
