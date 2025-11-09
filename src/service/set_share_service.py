from fastapi import HTTPException,status

from ErrorHandling.decorator import handle_errors
from InputResponseSchema.set_share_schema import ResponseSetShareSchema
from infrastructure.BaseService import  BaseService
from repository.Vendor import RepositoryVendor
import logging

logger = logging.getLogger(__name__)
class SetShareService(BaseService):

    def __init__(self,vendor_id , num):
         self.vendor_id = vendor_id
         self.num = num

    # @handle_errors
    async def get_fetch_data(self,vendor_id):
        vendor_id=int(vendor_id)
        query_vendor = await RepositoryVendor.get_and_check_entity(
            identifier=vendor_id,
        )
        percent = self.num / 100

        if query_vendor[0].get('share') != None:
            update_share =await RepositoryVendor.update_return_by_id(identifier=vendor_id,attributes= {'share':query_vendor[0].get('share')})
            if not update_share:
                logger.error(f"update_share {update_share}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='update is not successful')
            return update_share

        update_share = await RepositoryVendor.update_by_id(self.vendor_id, {'share': percent})
        print(update_share, '\n', 'hi hossein')

        return update_share

    @handle_errors
    def response(self,data):

        show = ResponseSetShareSchema(**data.__dict__)

        return  show

    @handle_errors
    async def process(self):
        data =await self.get_fetch_data(self.vendor_id)
        print(data)
        response = self.response(data)
        return  response

    @handle_errors
    def validate(self):
        pass
