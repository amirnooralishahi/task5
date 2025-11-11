from infrastructure.BaseService import BaseService
from repository.Customer import RepositoryCustomer
from repository.Invoice import RepositoryInvoice
from repository.parcelItem import RepositoryItem
from repository.parcelRepo import RepositoryParcel
from repository.product import RepositoryProduct


class GetShowItemToCustomerService(BaseService):

    def __init__(self, name, last_name):
        self.name = name
        self.last_name = last_name

    async def validate(self):
        pass

    async def process(self):
        await self.validate()
        await self.fetch_data()
        await self.fetch_data_parcel_item()
        return  self.response()

    async def fetch_data(self):
        customer = await RepositoryCustomer.get_and_check_entity(identifier=self.name,
                                                                 field_name='name',
                                                                 last_name=self.last_name)
        id_customer = customer[0].get('id')
        Invoice = await RepositoryInvoice.get_and_check_entity(
            identifier=id_customer,
            field_name= 'customer_id'
        )
        id_invoice = [value.get('id') for value in Invoice]
        parcel = await RepositoryParcel.get_and_check_entity(
            identifier=id_invoice,
            field_name='invoice_id'
        )

        return parcel



    async def response(self):
        data = await self.fetch_data()
        return data