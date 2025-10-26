from decimal import Decimal

from pydantic import BaseModel



class ShowPostVendor(BaseModel):

    price_delivery: Decimal
    parcel_id : int
    name_customer : str
    lastName_customer : str
    statusDelivery : str

