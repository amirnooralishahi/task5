from src.repository.Customer import RepositoryCustomer
from src.repository.Invoice import RepositoryInvoice
from src.repository.parcelItem import RepositoryItem
from src.repository.parcelRepo import RepositoryParcel
from src.repository.product import RepositoryProduct
from InputResponseSchema.get_show_item_to_vendor_schema import ShowParcel


class getShowItemToCustomer:
    def __init__(self,name,last_name):
        self.name=name
        self.last_name=last_name
    async def process(self):
        query_customer =await RepositoryCustomer.get_and_check_entity(
            RepositoryCustomer,
            identifier=self.name,
            field_name='name',
            last_name=self.last_name
        )
        execute = await RepositoryInvoice.get_and_check_entity(
            RepositoryInvoice,
            identifier=query_customer[0].get('id'),
            field_name='customer_id',
        )
        invoice_id = execute[0].get('id')
        execute_parcel = await RepositoryParcel.get_and_check_entity(
            RepositoryParcel,
            identifier=invoice_id,
            field_name='invoice_id',
        )
        show_list = []

        saveParcelId = [value['id'] for value in execute_parcel]
        execute_item = await RepositoryItem.get_and_check_entity(
            RepositoryItem,
            identifier=saveParcelId,
            field_name='parcel_id'
        )
        count = execute_item[0].get('count')
        get_product = RepositoryProduct.select_where(
            RepositoryProduct.field('id').eq(execute_item[0].get('product_id'))).select('*')
        execute_item = await RepositoryProduct.execute_and_fetch(get_product)
        name = execute_item[0].get('name')
        price = (execute_item[0].get('price'))
        show = ShowParcel(
            id=saveParcelId,
            TotalPrice=execute_parcel[0].get('price'),
            price=price,
            nameProduct=name,
            count=count,
            status=execute_parcel[0].get('status'),
            origin=execute_parcel[0].get('origin')
        )
        show_list.append(show)

        return show_list