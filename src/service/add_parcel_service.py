from datetime import datetime

from fastapi import HTTPException
from typing import Optional


from repository.Vendor import RepositoryVendor
from repository.product import RepositoryProduct
from schema.SchemaAddItem import AddProductItem
from schema.SchemaProduct import addProduct
from src.Enum.changeCode import BaseProcess
from pydantic import BaseModel







class addProductByVendor(BaseProcess):

    def __init__(self,name:str ,last_name:str ,data:dict ):
        self.name = name
        self.last_name = last_name
        self.data = data


    async  def validate_data(self):
        try:
            self.vendor=await RepositoryVendor.get_and_check_entity(
                identifier=self.name ,
                field_name='name',
                last_name=self.last_name
            )
        except ValueError as e:
            raise HTTPException(status_code=404 , detail=f'this vendor does not exist-{e}')

        return  self.vendor


    async def process_data(self):
        value_product = {
            'vendor_id':self.vendor[0].get("id"),
            'name':self.data.get('parcel').get('nameProduct'),
            'count':self.data.get('parcel').get('count'),
            'price':self.data.get('parcel').get('price'),
             'created_at':datetime.now()
        }
        try:
            create_product =await RepositoryProduct.create_return(value_product)
            show= addProduct(
                **create_product
            )
            return  show
        except ValueError as e:
            raise HTTPException(status_code=404, detail=f'create product failed{e}')




class addInvoiceService(BaseProcess):
    def __init__(self,**kwargs ):
        pass
    def validate_data(self):
        pass
    def process_data(self):
        pass
    def execute(self):
        pass

class addParcelItemService(BaseProcess):
    def __init__(self,**kwargs ):
        pass
    def validate_data(self):
        pass
    def process_data(self):
        pass
    def execute(self):
        pass
