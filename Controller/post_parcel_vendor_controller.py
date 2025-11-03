from Enum.EnumInvoice import EnumInvoice
from hepler.helper_parcel import get_and_check_entity
from repository.Customer import RepositoryCustomer
from repository.Vendor import RepositoryVendor
from repository.parcelRepo import RepositoryParcel
from schema.SchemaSendPostVendor import ShowPostVendor


class PostParcelVendorController:


    def __init__(self,name,last_name):
        self.name = name
        self.last_name = last_name


    async def process(self):
        execute = await get_and_check_entity(
            RepositoryVendor,
            identifier=self.name,
            field_name='name',
            last_name=self.last_name
        )
        constFinally = 0

        execute_parcel = await get_and_check_entity(
            RepositoryParcel,
            identifier=execute[0].get('id'),
            field_name='vendor_id'
        )

        id_invoice = [value.get('invoice_id') for value in execute_parcel]
        execute_parcel_all = await  get_and_check_entity(
            RepositoryParcel,
            identifier=id_invoice,
            field_name='invoice_id'
        )

        priceDelivery = [constFinally + value.get('pricedelivery') for value in execute_parcel_all if
                         value.get('pricedelivery') is not None]
        DeliveryStatus = [value.get('delivery') for value in execute_parcel_all if
                          value.get('delivery') == 'مرسوله توسط غرفه دار ارسال شد ']
        id_parcel = [value.get('id') for value in execute_parcel]
        for id in id_parcel:
            update = await RepositoryParcel.update_by_id(id, {'delivery': EnumInvoice.PARCEL_SEND_BY_VENDOR,
                                                              'pricedelivery': 30000})

        customer_id = [value.get('customer_id') for value in execute_parcel]
        query_customer = await get_and_check_entity(
            RepositoryCustomer,
            identifier=customer_id,
        )
        name_customer = [value.get('name') for value in query_customer]
        last_name_customer = [value.get('last_name') for value in query_customer]
        id_vendor = [value.get('id') for value in execute]
        return ShowPostVendor(
            price_delivery=priceDelivery,
            parcel_id=id_parcel,
            name_customer=name_customer,
            lastName_customer=last_name_customer,
            statusDelivery=DeliveryStatus
        )