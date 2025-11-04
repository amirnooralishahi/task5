from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING, Any, List, Dict
from models.model_abstract import ModelAbstract



class productModel(ModelAbstract):
    def repository(self) -> Any:
         from repository.product import RepositoryProduct
         return RepositoryProduct

    id: int
    name :str
    vendor_id :int
    price : int

    def vendor(self):
        return  self.relation('vendor')
