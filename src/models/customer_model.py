from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING, Any, List, Dict
from src.models.model_abstract import ModelAbstract



class customer(ModelAbstract):
    def repository(self) -> Any:
        from src.repository.Customer import RepositoryCustomer
        return RepositoryCustomer
    id :int
    name : str
    last_name : str
    balance: Decimal
    national_code: int
    phone :int
    city : str
