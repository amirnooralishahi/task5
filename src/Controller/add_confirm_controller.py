from fastapi import HTTPException,status
from typing import Union, List
from ErrorHandling.Exeption import UpdateFailedError
from src.Enum.EnumInvoice import EnumInvoice
from responseSchema.add_confirm import AddConfirm
from src.repository.parcelRepo import RepositoryParcel


class addConfirm:
    def __init__(self,parcel_id:Union[List[int],int]):
        self.parcel_id = parcel_id


    def validate(self)->list:
        try:
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
            return parcel_ids
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f'error during validate add confirm  {e}')
    async def get_data(self,parcel_ids):
        try:
            query_parcel = await RepositoryParcel.get_and_check_entity(
                RepositoryParcel,
                identifier=parcel_ids,
            )
            change_status = await RepositoryParcel.update_by_id(query_parcel[0].get('id'),
                                                                {'status': EnumInvoice.PARCEL_CONFIRM_BY_VENDOR})
            if not change_status:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='process update is not successfully')

            return  change_status
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f'')


    def response(self,data)->dict:
        try:
            data = data
            res=AddConfirm(**data)
            return res
        except Exception as e:
            raise UpdateFailedError(e)


    async def process(self):
        parcel_ids = self.validate()
        data = await self.get_data(parcel_ids)
        return  self.response(data)
