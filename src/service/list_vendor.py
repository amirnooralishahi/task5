from tkinter.font import names

from infrastructure.BaseService import BaseService
from repository.Vendor import RepositoryVendor
from fastapi import HTTPException,status

from schema.SchemaVendor import ShowVendorSchema


class ListVendorService(BaseService):

    def __init__(self):
        pass

    def validate(self):
        pass

    async def fetch_data(self):

        vendor = await RepositoryVendor.all()
        if not vendor:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='problem is available ')

        if not vendor :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='problem is available ')
        return vendor



    async def process(self):
        database = await self.fetch_data()
        print(database)
        return database


