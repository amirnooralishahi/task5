from infrastructure.BaseService import BaseService
from repository.Customer import RepositoryCustomer
from fastapi import HTTPException , status
from repository.parcelRepo import RepositoryParcel
from InputResponseSchema.cancel_one_parcel_schema import ResponseCancelOneParcel

class CancelOneParcelService(BaseService):


    def __init__(self,name ,last_name , parcel_id):
        self.name = name
        self.last_name =last_name
        self.parcel_id = parcel_id

    async def validate(self):
        if not isinstance(self.name , str ):
            raise TypeError('name must be a string')
        if not isinstance(self.last_name , str ):
            raise TypeError('last_name must be a string')





    async def process(self):
        await self.validate()
        await self.setup()
        await self.fetch_data()
        return  await self.response()
    async def setup(self):
        check_customer=await RepositoryCustomer.get_customer(
            self.name , self.last_name
        )
        if not check_customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user not found')
        else :
            sender = 'مشتری'

        return  sender


    async def fetch_data(self):
        fetch_data_parcel = await RepositoryParcel.get_and_check_entity(
            self.parcel_id
        )
        id_parcel = fetch_data_parcel[0].get('id')
        sender = await self.setup()
        await RepositoryParcel.update_by_id(id_parcel,{'status': f'{sender}کنسل شده توسط '})
        return  fetch_data_parcel

    async def response(self):
        data =await self.fetch_data()
        show = ResponseCancelOneParcel(id=data[0].get('id'),
                                       price =data[0].get('price'),
                                       status =data[0].get('status'))
        return show