from pydantic import BaseModel, constr, condecimal, field_validator
from decimal import Decimal, ROUND_HALF_UP
from typing import List


class InputCancelInvoice(BaseModel):
    name: str
    last_name: str
    invoice_id: int


class ShowCancelParcelWithInvoice(BaseModel):
    id: int
    vendor_id: int
    price: condecimal(max_digits=12, decimal_places=2)
    count: int
    origin: constr(min_length=2)
    pricedelivery: condecimal(max_digits=12, decimal_places=2)

    @field_validator("price", "pricedelivery", mode="before")
    def normalize_decimal(cls, v):
        if isinstance(v, Decimal):
            return v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if v is None:
            return 0
        return Decimal(v)


class ResponseCancelInvoice(BaseModel):
    invoice_id: int
    customer_id: int
    list_parcel: List[ShowCancelParcelWithInvoice]
    status: constr(min_length=5)
