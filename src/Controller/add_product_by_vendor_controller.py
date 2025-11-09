from ValidatePydantic.Schemaproduct import validateVendor
from infrastructure.controller import BaseController
from InputResponseSchema.add_product import ResponseAddProduct
from src.service.add_product_service import AddProductByVendorService
from fastapi import HTTPException ,status
class AddProductByVendor(BaseController):


    def __init__(self,name:str,last_name:str,data:validateVendor):
        self.name=name
        self.last_name=last_name
        self.__data=data





    async def process(self):
        try:
            add_prodcut=AddProductByVendorService(
                name=self.name,
                last_name=self.last_name,
                data=self.__data

            ).process()
            response = self.response(add_prodcut)
            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def response(self,data):

                show = ResponseAddProduct(
                    **data
                )
                response = show
                return response


