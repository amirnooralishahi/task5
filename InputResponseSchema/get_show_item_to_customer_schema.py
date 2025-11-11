from pydantic import BaseModel ,condecimal,constr


class InputGetShowItemToCustomerSchema(BaseModel):
    name:str
    last_name :str




class ResponseGetSHowItemToCustomerSchema(BaseModel):
    id :int
    TotalPrice :condecimal(max_digits=12, decimal_places=2)
    count :int
    status :constr(min_length=5)
    origin :constr(min_length=2)

