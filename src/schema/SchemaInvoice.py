from typing import Optional

from pydantic import BaseModel,Json
from decimal import Decimal


class CreateInvoiceSchema(BaseModel):

    customer_id : int
    status:Optional[str]
