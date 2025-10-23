from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING, Any, List, Dict
from models.model_abstract import ModelAbstract


class vendor(ModelAbstract):

    def repository(self) -> Any:
        from repository.Vendor import RepositoryVendor
        return RepositoryVendor

    id: Optional[int]
    name: str
    last_name: str
    phone: Optional[int]
    balance: Optional[int]
    national_code: Optional[int]
    city: Optional[str]

    def parcel_relation(self):
        from repository.Vendor import RepositoryVendor
        from repository.parcelRepo import RepositoryParcel

        return RepositoryVendor.has_many(RepositoryParcel, 'vendor_id', 'id')



