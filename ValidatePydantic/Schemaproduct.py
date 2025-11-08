
from pydantic import BaseModel,constr





class validateVendor(BaseModel):

    name:constr(strip_whitespace=True,min_length=1)
    last_name :constr(strip_whitespace=True,min_length=1)


