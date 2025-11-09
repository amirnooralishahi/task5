from pydantic import BaseModel ,constr,condecimal





class ResponseAllList(BaseModel):
    name_vendor:constr(min_length=2)
    last_name_vendor:constr(min_length=2)
    name_product:constr(min_length=2)
    price:condecimal(ge=100,max_digits=10, decimal_places=2)