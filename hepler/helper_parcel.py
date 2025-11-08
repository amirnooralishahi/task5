from http.client import HTTPException
from typing import Type, Any, List, Dict

from src.Enum.EnumInvoice import EnumInvoice
from orm.src.backbone_orm import Parameters
from orm.src.backbone_orm.repository_abstract import RepositoryAbstract
from src.repository.Customer import RepositoryCustomer
from src.repository.parcelItem import RepositoryItem
from src.repository.parcelRepo import RepositoryParcel
from fastapi import HTTPException,status

from src.repository.product import RepositoryProduct



async def get_and_update(repository: Type[RepositoryAbstract],
                         identifier=Any,
                         field_name: str = 'id',
                         dict_update= Any,
                         ):

    if isinstance(identifier,list) :
        params = Parameters()
        query =await repository.update_where_in(
            field=field_name,
            identifiers=(identifier),
            attributes=dict_update
        )
        print(query)
    elif isinstance(identifier,int):
        query =await repository.update_by_id(
            int(identifier),
            dict_update
       )
        print(query)


    print(query)

    return query


async def get_item_and_product_details(parcel_id: int):
    query_items = RepositoryItem.select_where(RepositoryItem.field('parcel_id').eq(parcel_id)).select('*')
    execute_items = await RepositoryItem.execute_and_fetch(query_items)

    if not execute_items:
        raise HTTPException(status_code=404, detail=' parcelItem is not exist')

    product_ids = [item.get('product_id') for item in execute_items]

    query_product = RepositoryProduct.select_where(RepositoryProduct.field('id').isin(product_ids)).select('*')
    execute_product = await RepositoryProduct.execute_and_fetch(query_product)
    execute_finally = {'products': execute_product[0], 'count': execute_items[0].get('count')}
    return execute_finally


async def check_and_buy_item(vendor_id:List[int]|int,
                             dict_product:dict
                             ,customer_id:int):



        product = await get_and_check_entity(RepositoryProduct,
                                             identifier=vendor_id,
                                             field_name='vendor_id',
                                             name=dict_product.get("name"))
        customer = await get_and_check_entity(RepositoryCustomer,
                                          identifier=customer_id)

        price = sum(dict_product.get('price'))
        print(int(customer.balance))
        if int(customer.balance) < price:
            print('balance1')
            raise HTTPException(status_code=404, detail='موجودی شما کافی نمی باشد')
        for index,value in enumerate(product):
                if (value.get('name') in dict_product.get("name")) :
                    index_number = dict_product.get("name").index(value.get('name'))

                    if (value.get('count') < dict_product.get('count')[index_number]):
                        print('balance2')

                        raise HTTPException(status_code=404,detail='موجودی محصول کافی نمی باشد')
                    else:
                        count=(value.get('count')-dict_product.get("count")[index_number])
                        await RepositoryProduct.update_by_id(value.get('id'),{'count':count})

        change_balance = int(customer.balance)-price
        await RepositoryCustomer.update_by_id(customer_id,{'balance':change_balance})
        return status.HTTP_200_OK
