from ErrorHandling.decorator import handle_errors
from InputResponseSchema.set_share_schema import ResponseSetShareSchema
from infrastructure.BaseService import  BaseService
from repository.Vendor import RepositoryVendor
from fastapi import HTTPException,status
import logging

logger = logging.getLogger(__name__)
class SetShareService(BaseService):

    def __init__(self,vendor_id , num):
         self.vendor_id = vendor_id
         self.num = num

    @handle_errors
    async def get_fetch_data(self):

        query_vendor = await RepositoryVendor.get_and_check_entity(
            identifier=self.vendor_id,
        )
        percent = self.num / 100

        if query_vendor.share != None:
            update_share =await RepositoryVendor.update_by_id(self.vendor_id, {'share': query_vendor.share})
            return update_share

        update_share = await RepositoryVendor.update_by_id(self.vendor_id, {'share': percent})
        return update_share

    @handle_errors
    def response(self,data):
        show = ResponseSetShareSchema(**data)
        return  show

    @handle_errors
    def process(self):
        data = self.get_fetch_data()
        response = self.response(data)
        return  response

    @handle_errors
    def validate(self):
        pass
