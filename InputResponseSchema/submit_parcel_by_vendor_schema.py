import datetime
from decimal import Decimal, ROUND_HALF_UP
from pydantic import BaseModel, condecimal, constr, conint, field_validator


class AddConfirm(BaseModel):
    price: condecimal(ge=1000, max_digits=10, decimal_places=2)
    share_company: condecimal(ge=100, max_digits=10, decimal_places=2)
    invoice_id: int
    updated_at: datetime.datetime
    created_at: datetime.datetime
    status: constr(min_length=10)
    origin: constr(min_length=2)
    count: conint(ge=1)
    delivery: constr(min_length=10)
    vendor_id: int
    pricedelivery: condecimal(ge=1000, max_digits=10, decimal_places=2)
    methodpost: constr(min_length=10)

    @field_validator("share_company", mode="before")
    def normalize_decimal(cls, v):
        if isinstance(v, Decimal):
            return v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return Decimal(v)
