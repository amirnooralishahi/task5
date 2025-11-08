from datetime import datetime

from fastapi import HTTPException
from typing import Optional

from hepler.helper_parcel import get_and_check_entity
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


    def validate_data(self):
        self.validate_data_product = addProduct(
            vendor_name=self.data.get('parcel').get('nameProduct'),
            vendor_last_name=self.data.get('parcel').get('lastName'),
            name_product=self.data.get('parcel').get('nameProduct'),
            count=self.data.get('parcel').get('count'),
            price = self.data.get('parcel').get('price')
        )
        try:
            return self.validate_data_product
        except :
            raise HTTPException(status_code=422, detail="this input is invalid")

    def execute(self):
        try:
            get_vendor = get_and_check_entity(
                RepositoryVendor ,
                identifier=self.validate_data_product.vendor_name ,
                last_name=self.validate_data_product.vendor_last_name
            )
            vendor_id = get_vendor[0].get('id')
            return vendor_id
        except AttributeError as e:
            raise HTTPException(status_code=404, detail=str(e))

    def process_data(self, vendor, data):
        value_product = {
            'vendor_id':vendor,
            'name':data.get('parcel').get('nameProduct'),
            'count':data.get('parcel').get('count'),
            'price':data.get('parcel').get('price'),
             'created_at':datetime.now()
        }
        try:
            create_product = RepositoryProduct.create_return(value_product)
            show= addProduct(
                **value_product
            )
            return  show
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))




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
