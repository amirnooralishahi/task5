from datetime import datetime
from decimal import Decimal

from ErrorHandling.decorator import handle_errors
from infrastructure.BaseService import BaseService
from repository.Vendor import RepositoryVendor
from fastapi import HTTPException , status
from repository.product import RepositoryProduct


class AddProductByVendorService(BaseService):


    def __init__(self,name,last_name,data):
        self.name=name
        self.last_name=last_name
        self.__data=data

    async def validate(self):
        pass
    @handle_errors
    async def process(self):
        await self.fetch_data()
        await self.add_product_by_vendor()
        return  await self.response()
    async def fetch_data(self):
        vendor = await RepositoryVendor.get_and_check_entity(
            identifier=self.name,
            field_name='name',
            last_name=self.last_name
        )
        value_product = {
            'vendor_id': vendor[0].get("id"),
            'name': self.__data.get('parcel').get('nameProduct'),
            'count': int(self.__data.get('parcel').get('number')),
            'price': Decimal(self.__data.get('parcel').get('price')),
            'created_at': datetime.now()
        }
        return  value_product

    async def add_product_by_vendor(self):
        value_product = await self.fetch_data()
        create_product = await RepositoryProduct.create_return(value_product)
        if not create_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='product not created'
            )

        query = RepositoryProduct.select_where(RepositoryProduct.field('id').eq(create_product.id)).select('*')
        execute_query = await RepositoryProduct.execute_and_fetch(query)
        if not execute_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='product not found')
        return execute_query[0]
    async def response(self):
        data = await self.add_product_by_vendor()
        return data