from datetime import datetime
from typing import Dict, Any
from ValidatePydantic.Schemaproduct import validateVendor

from src.repository.Vendor import RepositoryVendor
from src.repository.product import RepositoryProduct
from src.schema.SchemaAddItem import AddProductItem
from infrastructure.controller import BaseController
from src.service.add_product_service import addProductService

class addProductByVendor(BaseController):


    def __init__(self,name,last_name:validateVendor,data):
        self.name=name
        self.last_name=last_name
        self.__data=data



    def validate(self):
        pass

    async def process(self):
        try:
            addProdcut=addProductService(
                name=self.name,
                last_name=self.last_name,
                data=self.__data

            )

            return  await addProdcut.response()

        except Exception as e:
            print(e)
