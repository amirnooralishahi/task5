from src.repository.Invoice import RepositoryInvoice
from src.repository.parcelRepo import RepositoryParcel
from src.schema.SchemaParcel import SendProductToCustomerSchema


class sendProductToCustomerController:


    def __init__(self, parcel_id:int):
        self.parcel_id = parcel_id




    async def process(self):
        get_parcel =await RepositoryParcel.get_and_check_entity(
            RepositoryParcel,
            self.parcel_id,
            'id',
            'this parceel is not exist'
        )
        await RepositoryParcel.update_by_id(self.parcel_id , {'delivery':'ارسال شده توسط غرفه دار'})
        invoice_id = get_parcel[0].get('invoice_id')
        await RepositoryInvoice.get_and_check_entity(
            RepositoryInvoice,
            invoice_id,
            'id',
            'this invoice is not exist'
        )
        get_all_parcel =await RepositoryParcel.get_and_check_entity(
            RepositoryParcel,
            invoice_id,
            'invoice_id'
        )
        value= [await  RepositoryInvoice.update_by_id(invoice_id,{'delivery':'تمامی مرسوله های شما ارسال شده اند'})
                for index in get_all_parcel
                for value in index.values() if value =='ارسال شده توسط غرفه دار']

        return SendProductToCustomerSchema(
            vendor_id=get_parcel[0].get('vendor_id'),
            parcel_id=get_parcel[0].get('id'),
            invoice_id=get_parcel[0].get('invoice_id'),
            status=get_parcel[0].get('status')
        )
