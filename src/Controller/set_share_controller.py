from InputResponseSchema.set_share_schema import InputSetShareSchema
from service.set_share_service import SetShareService
from src.repository.Vendor import RepositoryVendor
from infrastructure.controller import BaseController


class SetShare(BaseController):

    def __init__(self,vendor_id:InputSetShareSchema,num:InputSetShareSchema):
        self.vendor_id = vendor_id
        self.num = num

    async def process(self):
        service = SetShareService(
            self.vendor_id,
            self.num
        )
        return await service.process()

