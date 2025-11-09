from service.send_product_to_customer_service import SendProductToCustomerService
from src.schema.SchemaParcel import SendProductToCustomerSchema


class SendProductToCustomerController:


    def __init__(self, parcel_id:int):
        self.parcel_id = parcel_id




    async def process(self):
        service = SendProductToCustomerService(
            self.parcel_id,
        )
        response =await self.response(await service.response())
        return  response

    def response(self,data):
        get_parcel = data
        show = SendProductToCustomerSchema(
            vendor_id=get_parcel[0].get('vendor_id'),
            parcel_id=get_parcel[0].get('id'),
            invoice_id=get_parcel[0].get('invoice_id'),
            status=get_parcel[0].get('status')
        )
        return show