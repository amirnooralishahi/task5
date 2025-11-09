from fastapi import HTTPException,status
from infrastructure.BaseService import BaseService
from repository.Vendor import RepositoryVendor
from repository.product import RepositoryProduct
from InputResponseSchema.all_list_product import ResponseAllList

class allListProductService(BaseService):

    async def validate(self):
        pass
    async def fetch_data(self):
        try:
            get_product = await RepositoryProduct.all()
            if not get_product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="problem is available")
            vendor_id = [value.id for value in get_product]
            info_vendor = await RepositoryVendor.get_and_check_entity(
                identifier=vendor_id,
                field_name='id'
            )
            if not info_vendor:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='vendor is not found')

            vendor = {id: {'nameVendor': value.get('name'), 'last_name_vendor': value.get('last_name'),
                           'name': pro.name, 'price': pro.price
                           }
                      for id, pro in enumerate(get_product)
                      for value in info_vendor if value.get('id') == pro.vendor_id

                      }
            return vendor
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    async def response(self):
        try:
            list_product =[]
            vendor=await self.fetch_data()
            for key, value in vendor.items():
                value = {
                    'name_vendor': value.get('nameVendor'),
                    'last_name_vendor': value.get('last_name_vendor'),
                    'name_product': value.get('name'),
                    'price': value.get('price'),
                }
                show=ResponseAllList(
                   **value
                )
                list_product.append(show)
            return list_product
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    async def process(self):
            return await self.response()






