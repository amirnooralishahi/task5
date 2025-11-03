from hepler.helper_parcel import get_and_check_entity, get_item_and_product_details
from repository.Customer import RepositoryCustomer
from repository.Vendor import RepositoryVendor
from repository.parcelRepo import RepositoryParcel
from schema.SchemaShowParcel import ShowCancelParcel


class cancelOneParcelController:
   def __init__(self,name,last_name,parcel_id):
       self.name = name
       self.last_name = last_name
       self.parcel_id = parcel_id


   async def process(self):
        query_customer = await RepositoryCustomer.get_customer(self.name, self.last_name)
        if query_customer:
            sender = 'مشتری'
        execute_vendor = await get_and_check_entity(
            RepositoryVendor,
            identifier=self.name,
            field_name='name',
            last_name=self.last_name
        )
        execute = await get_and_check_entity(
            RepositoryParcel,
            identifier=self.parcel_id,

        )

        update = await RepositoryParcel.update_by_id(self.parcel_id, {'status': f'{sender}کنسل شده توسط '})
        execute_product = await get_item_and_product_details(self.parcel_id)

        count = execute_product.get('count')
        price = execute_product.get('products').get('price')
        name = execute_product.get('products').get('name')

        return ShowCancelParcel(
            TotalPrice=execute.price,
            price=price,
            nameProduct=name,
            count=count,
            status=execute.status,
            origin=execute.origin,
            sender=sender
        )