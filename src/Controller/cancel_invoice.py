from fastapi import HTTPException

from src.Enum.EnumInvoice import EnumInvoice
from hepler.helper_parcel import get_and_check_entity
from src.repository.Customer import RepositoryCustomer
from src.repository.Invoice import RepositoryInvoice
from src.repository.parcelRepo import RepositoryParcel
from src.schema.SchemaShowParcel import ShowCancelInvoice


class cancelInvoice:

    def __init__(self,name,last_name,invoice):
        self.name = name
        self.last_name = last_name
        self.invoice_id = invoice



    async def process(self):
        execute_customer = await get_and_check_entity(
            RepositoryCustomer,
            identifier=self.name,
            field_name='name',
            last_name=self.last_name
        )
        query = await get_and_check_entity(
            RepositoryInvoice,
            identifier=self.invoice_id,
            field_name='id',
        )
        if execute_customer[0].get('id') != query.customer_id:
            raise HTTPException(status_code=405, detail='this invoice not for you')
        parcel_query = await get_and_check_entity(
            RepositoryParcel,
            identifier=self.invoice_id,
            field_name='invoice_id'
        )
        if query:
            await RepositoryInvoice.update_by_id(query.id, {'status': EnumInvoice.INVOICE_CANCEL})
            for item in parcel_query:
                await RepositoryParcel.update_by_id(item.get('id'), {'status': EnumInvoice.PARCEL_CANCEL})
            return ShowCancelInvoice(
                invoice_id=self.invoice_id,
                customer_name=execute_customer[0].get('name'),
                status=query.status,
            )