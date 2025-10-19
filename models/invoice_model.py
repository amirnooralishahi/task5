from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING, Any, List, Dict

from models.model_abstract import ModelAbstract



class invoice(ModelAbstract):
    def repository(self) -> Any:
        from repository.Invoice import RepositoryInvoice
        return RepositoryInvoice

    id : int
    customer_id : int
    status : str
    created_at : datetime
    updated_at : datetime

    def invoice(self):
        return  self.relation('customer')