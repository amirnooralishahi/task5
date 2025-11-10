from infrastructure.controller import BaseController
from src.service.cancel_one_parcel_service import CancelOneParcelService
class cancelOneParcelController(BaseController):
   def __init__(self,name,last_name,parcel_id):
       self.name = name
       self.last_name = last_name
       self.parcel_id = parcel_id


   async def process(self):
        service =CancelOneParcelService(self.name,self.last_name,self.parcel_id)
        return  await service.process()



