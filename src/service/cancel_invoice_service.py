from collections.abc import Mapping

from ErrorHandling.decorator import handle_errors
from infrastructure.BaseService import BaseService
from fastapi import HTTPException, status, Response
from InputResponseSchema.cancel_invoice_schema import ResponseCancelInvoice
from repository.Customer import RepositoryCustomer
from repository.Invoice import RepositoryInvoice
from repository.parcelRepo import RepositoryParcel
from Enum.EnumInvoice import EnumInvoice


def to_dict(obj):
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "__dict__"):
        return vars(obj)
    if hasattr(obj, "_asdict"):
        return obj._asdict()
    if isinstance(obj, Mapping):
        return dict(obj)
    raise TypeError(f"Cannot convert {type(obj)} to dict")
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
        await self.get_cancel_all_parcel()
        return await self.response()

    async def fetch_data(self):
        execute_customer = await RepositoryCustomer.get_and_check_entity(

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

    async def get_cancel_all_parcel(self):
        data = await self.update_status_invoice()
        list_parcel = []
        self.validate_empty(data)
        parcel = await RepositoryParcel.get_parcel(invoice_id=data.id)
        id_parcel = [value.id for value in parcel]
        query = await RepositoryParcel.get_and_update_entity(identifier=id_parcel,
                                                             attributes={'status': EnumInvoice.INVOICE_CANCEL})
        list_parcel.append(query)
        return list_parcel


    async def response(self):
        data_update_invoice = await self.update_status_invoice()
        data_update_parcel = await self.get_cancel_all_parcel()
        print(data_update_parcel)
        if isinstance(data_update_parcel, list) and len(data_update_parcel) == 1 and isinstance(data_update_parcel[0],
                                                                                                list):
            data_update_parcel = data_update_parcel[0]

        if not isinstance(data_update_parcel, list):
            data_update_parcel = [data_update_parcel]
        for parcel in data_update_parcel:
            print(to_dict(parcel).get('x_original'))
        list_parcel = [to_dict(parcel).get('x_original')for parcel in data_update_parcel]
        print(list_parcel)
        return ResponseCancelInvoice(
            invoice_id=data_update_invoice.id,
            customer_id=data_update_invoice.customer_id,
            list_parcel=list_parcel,
            status=EnumInvoice.INVOICE_CANCEL
        )

    def validate_empty(self, data):
        if not data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"cancel this invoice not successfully")
