from datetime import datetime
from typing import Optional

from pydantic import BaseModel




class ShowInvoice(BaseModel):

    id: Optional[int]
    customer_id: Optional[int]
    status: str
    created_at: datetime
    updated_at: datetime


