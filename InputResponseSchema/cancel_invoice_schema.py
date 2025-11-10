from pydantic import BaseModel, constr, condecimal, field_validator
from decimal import Decimal, ROUND_HALF_UP


class ShowCancelParcelWithInvoice(BaseModel):
    parcel_id: int
    vendor_id: int
    price: condecimal(max_digits=12, decimal_places=2)
    count: int
    origin: constr(min_length=2)
    pricedelivery: condecimal(max_digits=12, decimal_places=2)

    @field_validator("share_company", mode="before")
    def normalize_decimal(cls, v):
        if isinstance(v, Decimal):
            return v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return Decimal(v)


class ShowCancelInvoice(BaseModel):
    invoice_id: str
    customer_id: str
    list_parcel: ShowCancelParcelWithInvoice
    status: constr(min_length=5)
