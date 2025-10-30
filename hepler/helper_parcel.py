from http.client import HTTPException
from typing import Type, Any, List
from orm.src.backbone_orm.repository_abstract import RepositoryAbstract
from repository.parcelItem import RepositoryItem
from repository.parcelRepo import RepositoryParcel
from fastapi import HTTPException

from repository.product import RepositoryProduct


async def get_and_check_entity(repository: Type[RepositoryAbstract],
                               identifier: Any,
                               field_name: str = 'id',
                               error_message: str = 'Resource not found',
                               **kwargs: Any
                               ):
    if field_name == 'id' and hasattr(repository, 'find_by_id') and not kwargs and not isinstance(identifier, list):
        execute_get = await repository.find_by_id(identifier)


        if not execute_get:
            raise HTTPException(status_code=404, detail=error_message)
        return execute_get
    query = repository.select_query().select('*')

    if isinstance(identifier, list):
        query = query.where(repository.field(field_name).isin(identifier))
    else:

        query = query.where(repository.field(field_name).eq(identifier))

    if kwargs:
        for key, value in kwargs.items():
            if identifier is list:
                query = query.where(repository.field(key).isin(value))
            else:
                query = query.where(repository.field(key).eq(value))

    execute_query = await repository.execute_and_fetch(query)
    if not execute_query:
        raise HTTPException(status_code=404, detail=error_message)

    return execute_query


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
