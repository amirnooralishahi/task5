from ErrorHandling.decorator import handle_errors
from infrastructure.BaseService import BaseService
from fastapi import HTTPException, status, Response
from InputResponseSchema.cancel_invoice_schema import ShowCancelInvoice
from repository.Customer import RepositoryCustomer
from repository.Invoice import RepositoryInvoice
from repository.parcelRepo import RepositoryParcel
from Enum.EnumInvoice import EnumInvoice


class CancelInvoiceService(BaseService):

    def __init__(self, name: str, last_name: str, invoice):
        self.name = name
        self.last_name = last_name
        self.invoice_id = invoice

    async def validate(self):

        if isinstance(self.name, str) and isinstance(self.last_name, str):
            self.name = self.name.strip()
            self.last_name = self.last_name.strip()
        else:
            raise HTTPException(status_code=400, detail='name and/or last_name are required and them must be str')

        if isinstance(self.invoice_id, str):
            self.invoice_id = self.invoice_id.strip()
            self.invoice_id = int(self.invoice_id)

        if self.invoice_id < 0:
            raise HTTPException(status_code=400, detail='invoice_id must be greater than 0')

    @handle_errors
    async def process(self):
        await self.validate()
        await self.fetch_data()
        await self.update_status_invoice()
        await self.cancel_all_parcel()
        return await self.response()

    async def fetch_data(self):
        execute_customer = await RepositoryCustomer.get_and_check_entity(
            RepositoryCustomer,
            identifier=self.name,
            field_name='name',
            last_name=self.last_name
        )
        self.validate_empty(execute_customer)
        id_customer = execute_customer[0].get('id')
        query = await RepositoryInvoice.get_and_check_entity(
            identifier=self.invoice_id,
            field_name='id',

        )
        self.validate_empty(query)
        if query[0].get('customer_id') != id_customer:
            raise HTTPException(status_code=404, detail='this invoice and customer not match')

        return query[0]

    async def update_status_invoice(self):
        query = await self.fetch_data()
        id_invoice = query.get('id')
        self.validate_empty(query)
        update_invoice = await RepositoryInvoice.update_return_by_id(id_invoice, {"status": EnumInvoice.INVOICE_CANCEL})
        self.validate_empty(update_invoice)
        return update_invoice

    async def cancel_all_parcel(self):
        data = await self.update_status_invoice()
        list_parcel = []
        self.validate_empty(data)
        for item in data:
            self.validate_empty(item)
            parcel = await RepositoryParcel.update_return_by_id(item.get('id'), {'status': EnumInvoice.PARCEL_CANCEL})
            list_parcel.append(parcel)

        return list_parcel

    async def response(self):
        data_update_invoice = await self.update_status_invoice()
        data_update_parcel = await self.cancel_all_parcel()
        return ShowCancelInvoice(
            invoice_id=data_update_invoice[0].get('id'),
            customer_id=data_update_invoice[0].get('customer_id'),
            list_parcel=data_update_parcel,
            status=EnumInvoice.INVOICE_CANCEL
        )

    def validate_empty(self, data):
        if not data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"cancel this invoice not successfully")
