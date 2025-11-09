from fastapi import HTTPException,status
from typing import Union, List
from ErrorHandling.Exeption import UpdateFailedError
from ErrorHandling.decorator import handle_errors
from service.add_confirm_service import AddConfirmService
from src.Enum.EnumInvoice import EnumInvoice
from InputResponseSchema.add_confirm import AddConfirm
from src.repository.parcelRepo import RepositoryParcel


class submitParcelByVendorController:
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

    @handle_errors
    async def process(self):
        service = AddConfirmService(self.parcel_id)
        response= self.response(await service.response())
        return  response


    def response(self,data)->dict:
        try:
            data = data
            res=AddConfirm(**data)

        except Exception as e:
            raise UpdateFailedError(e)
        return res
