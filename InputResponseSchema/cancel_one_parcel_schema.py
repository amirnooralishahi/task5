from pydantic import BaseModel,condecimal,field_validator
from decimal import Decimal, ROUND_HALF_UP



class ResponseCancelOneParcel(BaseModel):
        id : int
        price : condecimal(max_digits=10, decimal_places=2)
        status : str

        @field_validator("price", mode="before")
        def normalize_decimal(cls, v):
            if isinstance(v, Decimal):
                return v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            elif v in None :
                return  0
            return Decimal(v)