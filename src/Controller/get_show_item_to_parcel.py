from hepler.helper_parcel import get_and_check_entity
from src.repository.Vendor import RepositoryVendor
from src.repository.parcelItem import RepositoryItem
from src.repository.parcelRepo import RepositoryParcel
from src.repository.product import RepositoryProduct
from src.schema.SchemaShowParcel import ShowParcel


class getShowItemToVendorController():
    def __init__(self, name,last_name):
        self.name=name ,
        self.last_name=last_name
    async def process(self):
                    execute = await get_and_check_entity(
                        RepositoryVendor,
                        identifier=self.name,
                        field_name='name',
                        error_message='this vendor is not exist',
                        last_name=self.last_name
                    )
                    id_vendor = [id['id'] for id in execute]
                    execute_parcel = await get_and_check_entity(
                        RepositoryParcel,
                        identifier=id_vendor,
                        field_name='vendor_id',
                        error_message='this parcel is not exist'
                    )
                    # print(execute_parcel)
                    list_product= []
                    id_parcelItem = [id['id'] for id in execute_parcel]

                    execute_item = await get_and_check_entity(
                        RepositoryItem,
                        identifier=id_parcelItem,
                        field_name='parcel_id',
                    )

                    id_product = [id['product_id'] for id in execute_item]
                    execute_product = await get_and_check_entity(
                        RepositoryProduct,
                        identifier=id_product,

                    )

                    name_product=[value['name'] for value in execute_product]
                    price_product=[value['price'] for value in execute_product]

                    for value in execute_parcel:
                        id= value['id']
                        price_parcel=value['price']
                        count_parcel = value['count']
                        status_parcel = value['status']
                        origin_parcel = value['origin']

                        show = ShowParcel(
                            id = id,
                            TotalPrice =price_parcel,
                            price = price_product,
                            nameProduct = name_product,
                            count = count_parcel,
                            status= status_parcel,
                            origin = origin_parcel
                        )
                        list_product.append(show)
                    return list_product