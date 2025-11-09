from ErrorHandling.decorator import handle_errors
from InputResponseSchema.get_show_item_to_vendor_schema import ShowParcel
from infrastructure.BaseService import BaseService
from repository.Vendor import RepositoryVendor
from repository.parcelItem import RepositoryItem
from repository.parcelRepo import RepositoryParcel
from repository.product import RepositoryProduct


class GetShowItemToVendorService(BaseService):
    def __init__(self,name,last_name):
        self.name = name
        self.last_name = last_name
    @handle_errors
    async def process(self):
        data = await self.fetch_data(self.name,self.last_name)
        return await self.response()
    async def response(self):
        data = await self.fetch_data(self.name,self.last_name)
        product = data.get("product")
        parcel = data.get('parcel')
        print(product,'\n')
        print(parcel,'\n')
        name_product = [value['name'] for value in product]
        price_product = [value['price'] for value in parcel]
        list_product =[]
        for value in parcel:
            id = value['id']
            price_parcel = value['price']
            count_parcel = value['count']
            status_parcel = value['status']
            origin_parcel = value['origin']

            show = ShowParcel(
                id=id,
                TotalPrice=price_parcel,
                price=price_product,
                nameProduct=name_product,
                count=count_parcel,
                status=status_parcel,
                origin=origin_parcel
            )
            list_product.append(show)
        return list_product

    def validate(self):
        pass
    @handle_errors
    async def fetch_data(self,name,last_name):
        execute = await RepositoryVendor.get_and_check_entity(
            identifier=self.name,
            field_name='name',
            error_message='this vendor is not exist',
            last_name=self.last_name
        )
        id_vendor = [id['id'] for id in execute]
        execute_parcel = await RepositoryParcel.get_and_check_entity(
            identifier=id_vendor,
            field_name='vendor_id',
            error_message='this parcel is not exist'
        )
        id_parcelItem = [id['id'] for id in execute_parcel]

        execute_item = await RepositoryItem.get_and_check_entity(
            identifier=id_parcelItem,
            field_name='parcel_id',
        )

        id_product = [id['product_id'] for id in execute_item]
        execute_product = await RepositoryProduct.get_and_check_entity(
            identifier=id_product,
        )

        response={
            'product': execute_product,
            'parcel': execute_parcel,
        }

        return  response