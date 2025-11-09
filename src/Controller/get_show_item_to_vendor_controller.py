from service.get_show_item_to_vendor_service import GetShowItemToVendorService
from infrastructure.controller import BaseController

class getShowItemToVendorController(BaseController):

    def __init__(self, name,last_name):
        self.name=name ,
        self.last_name=last_name

    async def process(self):
        service = GetShowItemToVendorService(name=self.name,last_name=self.last_name)
        return await service.process()