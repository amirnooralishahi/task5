from datetime import datetime
from decimal import Decimal
from infrastructure.BaseService import BaseService
from repository.Vendor import RepositoryVendor
from fastapi import HTTPException , status

from repository.product import RepositoryProduct
from responseSchema.addProduct import ResponseAddProduct


class addProductService(BaseService):


    def __init__(self,name,last_name,data):
        self.name=name
        self.last_name=last_name
        self.__data=data

    async def validate(self):
        try:
            self.vendor = await RepositoryVendor.get_and_check_entity(
                identifier=self.name,
                field_name='name',
                last_name=self.last_name
            )
            print(self.vendor)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'this vendor does not exist-{e}')

        return self.vendor

    async def process(self):
        vendor=await self.validate()
        value_product = {
            'vendor_id': vendor[0].get("id"),
            'name': self.__data.get('parcel').get('nameProduct'),
            'count': int(self.__data.get('parcel').get('number')),
            'price': Decimal(self.__data.get('parcel').get('price')),
            'created_at': datetime.now()
        }
        try:
            create_product = await RepositoryProduct.create_return(value_product)
            query=RepositoryProduct.select_where(RepositoryProduct.field('id').eq(create_product.id)).select('*')
            execute_query=await RepositoryProduct.execute_and_fetch(query)



            show = ResponseAddProduct(
                **execute_query[0]
            )

            return show
        except ValueError as e:
            raise HTTPException(status_code=404, detail=f'create product failed{e}')


    async def response(self):
        response = await self.process()
        return  response

