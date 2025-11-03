from datetime import datetime
from typing import Dict, Any

from hepler.helper_parcel import get_and_check_entity
from repository.Vendor import RepositoryVendor
from repository.product import RepositoryProduct


class addProductByVendor:


    def __init__(self,name:str,last_name:str, data: Dict[str, Any]):
        self.name=name
        self.last_name=last_name
        self.data=data


    async def process(self):
        get_vendor = await get_and_check_entity(
            RepositoryVendor,
            identifier=self.name,
            field_name='name',
            last_name=self.last_name
        )
        valueProduct = {
            'vendor_id': get_vendor[0].get("id"),
            'name': self.data.get('parcel').get('nameProduct'),
            'count': int(self.data.get('parcel').get('number')),
            'price': int(self.data.get('parcel').get('price')),
            'created_at': datetime.now(),
        }
        addProduct = await RepositoryProduct.create_return(valueProduct)
