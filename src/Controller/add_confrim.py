from types import NoneType

from fastapi import HTTPException
from typing import Union, List

from ErrorHandling.Exeption import UpdateFailedError
from src.Enum.EnumInvoice import EnumInvoice
from hepler.helper_parcel import get_and_check_entity
from src.repository.parcelRepo import RepositoryParcel


class addConfrim:
    def __init__(self,parcel_id:Union[List[int],int]):
        self.parcel_id = parcel_id

    async def process(self):
        if isinstance(self.parcel_id, str):
            parcel_ids = [int(p.strip()) for p in self.parcel_id.split(',') if p.strip().isdigit()]
        elif isinstance(self.parcel_id, list):
            parcel_ids = []
            for p in self.parcel_id:
                if isinstance(p, str) and ',' in p:
                    parcel_ids.extend([int(x.strip()) for x in p.split(',') if x.strip().isdigit()])

                elif str(p).isdigit():
                    parcel_ids.append(int(p))
        else:
            parcel_ids = []

        try:
            query_parcel = await get_and_check_entity(
                RepositoryParcel,
                identifier=parcel_ids,
            )
            change_status = await RepositoryParcel.update_by_id(query_parcel[0].get('id'),
                        {'status': EnumInvoice.PARCEL_CONFIRM_BY_VENDOR})
            return {'message': 'with successfully confer'}
        except AttributeError as e:
            return {'message': e}
        except UpdateFailedError as e:
            raise HTTPException(status_code=409,detail={'update not done '} )