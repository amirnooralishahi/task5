from pydantic import BaseModel ,constr,conint,condecimal




class InputSetShareSchema(BaseModel):
    vendor_id: int
    num: int


class ResponseSetShareSchema(BaseModel):
    name:str
    last_name: str
    city:str
    share:condecimal(max_digits=10, decimal_places=2)

