from infrastructure.BaseService import BaseService
from repository.Customer import RepositoryCustomer
from repository.Invoice import RepositoryInvoice
from repository.parcelItem import RepositoryItem
from repository.parcelRepo import RepositoryParcel
from repository.product import RepositoryProduct


class GetShowItemToCustomerService(BaseService):

    def __init__(self,name,last_name):
         self.name = name
         self.last_name = last_name

    async def validate(self):
        pass
    async def process(self):
        pass

    async def fetch_data_models(self):
        customer=await RepositoryCustomer.get_and_check_entity(identifier=self.name ,
                                                            field_name='name',
                                                            last_name=self.last_name)
        id_customer = customer.id
        Invoice = await RepositoryInvoice.get_and_check_entity(
            identifier=id_customer
        )
        id_invoice = Invoice.id
        parcel = await RepositoryParcel.get_and_check_entity(
            identifier=id_invoice ,
            field_name= 'invoice_id'
        )
        show_list =[]
        return parcel

    async def fetch_data_parcel_item(self):
        parcel = await self.fetch_data_models()
        parcel_id = [value['id'] for value in parcel]
        parcel_item = await RepositoryItem.get_and_check_entity(
            identifier=parcel_id,
            field_name='parcel_id'
        )
        count = parcel_item[0].get('count')
        product_id = [value.id for value in parcel_item]
        get_product = RepositoryProduct.select_where(
            RepositoryProduct.field('id').isin(product_id)).select('*')
        execute_get_product = RepositoryProduct.execute_and_fetch(get_product)
        product= {
            'count':count,
            'get_product':execute_get_product
        }
        return product

    async def response(self):
        pass