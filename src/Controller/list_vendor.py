from fastapi import HTTPException,status
from infrastructure.controller import BaseController
from src.schema.SchemaVendor import ShowVendorSchema
from src.service.list_vendor import  ListVendorService

class ListVendorController(BaseController):

    def __init__(self):
        pass

    def validate(self):
        pass
    async def process(self):
        try:
            controller =ListVendorService()
            service = controller.process()
            res =await self.response(service)
            return  res
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e))

    async def response(self,data_vendor):
        try:
            data =data_vendor
            list_vendor = []
            for item in  data :

                show = ShowVendorSchema(
                    id=item.id,
                    name=item.name,
                    last_name=item.last_name,
                    phone = item.phone,
                    balance = item.balance
                )
                list_vendor.append(show)
            return list_vendor
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e))