from ErrorHandling.decorator import handle_errors
from infrastructure.BaseService import  BaseService
from fastapi import HTTPException , status




class CancelInvoiceService(BaseService):

    def __init__(self,name:str,last_name:str , invoice):
            self.name =name
            self.last_name =last_name
            self.invoice_id = invoice

    async def validate(self):

        if isinstance(self.name , str) and isinstance(self.last_name ,str) :
            self.name = self.name.strip()
            self.last_name = self.last_name.strip()
        else:
            raise HTTPException(status_code=400, detail='name and/or last_name are required and them must be str')

        if isinstance(self.invoice_id , str) :
            self.invoice_id = self.invoice_id.strip()
            self.invoice_id = int(self.invoice_id)

        if self.invoice_id < 0 :
            raise HTTPException(status_code=400, detail='invoice_id must be greater than 0')






    @handle_errors
    async def process(self):
        pass

    async def response(self):
        pass


    async def fetch_data(self):
        pass
