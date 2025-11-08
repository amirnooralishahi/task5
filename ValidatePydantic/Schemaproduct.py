from datetime import datetime

from pydantic import BaseModel,conint,constr,condecimal



class inputProduct(BaseModel):
    name: constr(min_length=2)
    price:condecimal(ge=1000,max_digits=10,decimal_places=2)
    count: conint(ge=0)

class validateVendor(BaseModel):

    name:constr(strip_whitespace=True,min_length=1)
    last_name :constr(strip_whitespace=True,min_length=1)


