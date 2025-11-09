from datetime import datetime
from decimal import Decimal
from infrastructure.BaseService import BaseService
from repository.Vendor import RepositoryVendor
from fastapi import HTTPException , status

from repository.product import RepositoryProduct
from InputResponseSchema.add_product import ResponseAddProduct


class AddProductByVendorService(BaseService):


    def __init__(self,name,last_name,data):
        self.name=name
        self.last_name=last_name
        self.__data=data

    async def validate(self):
        pass

    async def process(self):
        data= await self.add_fetch_data()
        return data
    async def add_fetch_data(self):
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
        create_product = await RepositoryProduct.create_return(value_product)
        if not create_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='product not created'
            )
        query = RepositoryProduct.select_where(RepositoryProduct.field('id').eq(create_product.id)).select('*')
        self.execute_query = await RepositoryProduct.execute_and_fetch(query)
        if not self.execute_query:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='product not found')
        return  self.execute_query[0]



