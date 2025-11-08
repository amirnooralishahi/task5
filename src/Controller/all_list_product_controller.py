from service.all_list_product_service import allListProductService
from infrastructure.controller import BaseController



class AllListProductController(BaseController):

    def validate(self):
        pass

    async def process(self):
        service=allListProductService()
        return await service.process()
