from pydantic import BaseModel,condecimal,constr,conint,condate



class AddConfirm(BaseModel):

    price : condecimal(ge=1000,max_digits=10,decimal_places=2)
    share_company : condecimal(ge=100,max_digits=10,decimal_places=2)
    invoice_id : int
    updated_at: condate()
    created_at: condate()
    status : constr(min_length=10)
    origin: constr(min_length=2)
    count : conint(ge=1)
    delivery : constr(min_length=10)
    vendor_id : int
    pricedelivery: condecimal(ge=1000,max_digits=10,decimal_places=2)
    methodpost: constr(min_length=10)
