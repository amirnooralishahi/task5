from Enum.EnumInvoice import EnumInvoice
from ErrorHandling.decorator import handle_errors
from infrastructure.BaseService import BaseService
from repository.parcelRepo import RepositoryParcel
from fastapi import HTTPException, status


class AddConfirmService(BaseService):

    def __init__(self, parcel_id):
        self.parcel_ids = parcel_id

    def validate(self):
        pass

    @handle_errors
    async def process(self):
        await self.fetch_data()
        return self.response()

    async def response(self):
        data = await self.fetch_data()


    async def fetch_data(self):
        try:
            query_parcel = await RepositoryParcel.get_and_check_entity(
                RepositoryParcel,
                identifier=self.parcel_ids,
            )
            change_status = await RepositoryParcel.update_by_id(query_parcel[0].get('id'),
                                                                {'status': EnumInvoice.PARCEL_CONFIRM_BY_VENDOR})
            if not change_status:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='process update is not successfully')

            return change_status
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
