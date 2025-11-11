from infrastructure.controller import BaseController
from src.service.get_show_item_to_customer_service import GetShowItemToCustomerService
from InputResponseSchema.get_show_item_to_customer_schema import ResponseGetSHowItemToCustomerSchema
class GetShowItemToCustomer(BaseController):
    def __init__(self,name,last_name):
        self.name=name
        self.last_name=last_name
    async def process(self):
        service = GetShowItemToCustomerService(
            self.name,
            self.last_name
        )
        response = self.response(await service.response())
        return response
    def response(self,data):
        data = data
        list_parcel=[]
        for key,value in enumerate(data):
            show = ResponseGetSHowItemToCustomerSchema(
                id=value.get('id'),
                TotalPrice=value.get('price'),
                count=value.get('count'),
                status=value.get('status'),
                origin=value.get('origin'),
            )
            list_parcel.append(show)
        return list_parcel
