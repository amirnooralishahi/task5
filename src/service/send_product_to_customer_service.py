from infrastructure.BaseService import BaseService
from repository.Invoice import RepositoryInvoice
from repository.parcelRepo import RepositoryParcel


class SendProductToCustomerService(BaseService):
    def __init__(self,parcel_id):
        self.parcel_id = parcel_id
    def validate(self):
        pass

    async def process(self):
        await self.fetch_data()
        await self.update_data()

    async def fetch_data(self):
        get_parcel = await RepositoryParcel.get_and_check_entity(
            self.parcel_id,
            'id',
            'this parceel is not exist'
        )
        await RepositoryParcel.update_by_id(self.parcel_id, {'delivery': 'ارسال شده توسط غرفه دار'})
        invoice_id = get_parcel[0].get('invoice_id')
        await RepositoryInvoice.get_and_check_entity(
            invoice_id,
            'id',
            'this invoice is not exist'
        )
        get_all_parcel = await RepositoryParcel.get_and_check_entity(
            invoice_id,
            'invoice_id'
        )
        invoice = {'invoice':invoice_id,
                   'parcel':get_all_parcel[0]}
        return  invoice
    async def update_data(self):
        data = await self.fetch_data()
        invoice_id = data.get('invoice')
        get_all_parcel = data.get('parcel')
        value = [await  RepositoryInvoice.update_by_id(invoice_id, {'delivery': 'تمامی مرسوله های شما ارسال شده اند'})
                 for index in get_all_parcel
                 for value in index.values() if value == 'ارسال شده توسط غرفه دار']
        return  value

    async def response(self):
        data = await self.update_data()
        return  data


