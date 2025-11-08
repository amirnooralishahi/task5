import decimal
from datetime import datetime , timedelta

from typing import List, Dict, Any
from fastapi import HTTPException,status
from hepler.helper_parcel import check_and_buy_item, get_and_check_entity
from src.Enum.EnumInvoice import EnumInvoice
from src.repository.Customer import RepositoryCustomer
from src.repository.Invoice import RepositoryInvoice
from src.repository.Vendor import RepositoryVendor
from src.repository.parcelItem import RepositoryItem
from src.repository.parcelRepo import RepositoryParcel
from src.repository.product import RepositoryProduct
from src.schema.SchemaParcel import ProductParcelSchema
from ..kafkaProject.expirationParcel import kafka


class addItemParcel:

    def __init__(self,name,last_name ,data):
        self.name=name ,
        self.last_name=last_name
        self.data=data

    def __make_invoice_data(self):
        structured_data = {}
        list_product = []

        for key, value in self.data.get('data').items():
            structured_data[key] = value
        for vendor, choice_product in structured_data.items():
            name_vendor = vendor.split('-')[0]
            last_name_vendor = vendor.split('-')[1]
            for item in choice_product:
                list_product.append({
                    'vendor_name': name_vendor,
                    'vendor_last_name': last_name_vendor,
                    'nameProduct': item.get('product_name'),
                    'price': item.get('price'),
                    'count': item.get('count'),
                })

    async def process(self):

        get_customer = await get_and_check_entity(
            RepositoryCustomer,
            identifier=self.name,
            field_name='name',
            last_name=self.last_name
        )

        customer_id = get_customer[0].get('id')
        customer_origin = get_customer[0].get('city')
        get_invoice = await RepositoryInvoice.get_invoice(customer_id=customer_id)
        day_ago = datetime.now() - timedelta(days=1)

        value_invoice = {
            'customer_id': customer_id,
            'status': EnumInvoice.INVOICE_AWAIT_FOR_CONFIRM,
        }

        if not get_invoice:
            get_invoice = await RepositoryInvoice.create_return(value_invoice)

        elif day_ago.day > get_invoice[-1].created_at.day:
            get_invoice = await RepositoryInvoice.create_return(value_invoice)

        self.__make_invoice_data()

        total_amount = 0
        total_item_count = 0
        total_share_company = decimal.Decimal(0)
        productive: List[Dict[str, Any]] = []
        vendor_name = [key.split('-')[0] for key, value in structured_data.items()]
        vendor_last_name = [key.split('-')[1] for key, value in structured_data.items()]
        vendor_info = await get_and_check_entity(
            RepositoryVendor,
            identifier=vendor_name,
            field_name='name',
            last_name=vendor_last_name
        )
        vendor_share_map = {
            v.get('id'): v.get('share') for v in vendor_info
        }

        vendor_id_list = [value.get('id') for value in vendor_info]
        item_price = [int(item.get("price"))
                      for vendor, products_list in structured_data.items()
                      for item in products_list]
        name_product = [value.get('product_name')
                        for vendor, products_list in structured_data.items()
                        for value in products_list]
        item_count = [int(item.get('count'))
                      for vendor, products_list in structured_data.items()
                      for item in products_list]

        product = await get_and_check_entity(
            RepositoryProduct,
            identifier=name_product,
            field_name='name',
            vendor_id=vendor_id_list
        )
        product_map = {
            (p.get('name'), p.get('vendor_id')): p for p in product
        }

        sum_total_price = []
        sum_count_product = []
        sum_share_company = []
        dictProduct = {'name': name_product,
                       'price': item_price,
                       'count': item_count}
        update = await check_and_buy_item(vendor_id_list, dictProduct, customer_id)
        if update != status.HTTP_200_OK:
            raise HTTPException(status_code=406, detail='موجودی کافی نیست')
        current_vendor_items: List[Dict[str, Any]] = []

        last_vendor_id = []
        productive = []
        production = {}
        for item in list_product:

            vendor_id = next(
                (v.get('id') for v in vendor_info if
                 v.get('name') == item['vendor_name'] and v.get('last_name') == item['vendor_last_name']),
                None
            )

            if vendor_id is None:
                raise HTTPException(status_code=400, detail=f"غرفه دار {item['vendor_name']} یافت نشد.")

            if last_vendor_id is not None and vendor_id != last_vendor_id:

                if production.get('vendor_id') is not None:
                    productionUpdate_prev = {
                        'customer_id': customer_id,
                        'price': sum(sum_total_price),
                        'count': sum(sum_count_product),
                        'share_company': sum(sum_share_company),
                        'invoice_id': get_invoice[0].id,
                        'created_at': datetime.now(),
                        'origin': customer_origin,
                        'status': EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM,
                        'delivery': EnumInvoice.STATUS_DELIVERY,
                        'methodpost': EnumInvoice.METHOD_POST,
                        'vendor_id': last_vendor_id
                    }
                    production.update(productionUpdate_prev)
                    productive.append(production.copy())

                    sum_total_price = []
                    sum_count_product = []
                    sum_share_company = []
                    production = {}

            vendor_share_rate = vendor_share_map.get(vendor_id, 0)

            product_key = (item['nameProduct'], vendor_id)
            db_product = product_map.get(product_key)

            if not db_product:
                raise HTTPException(status_code=400, detail=f"محصول {item['nameProduct']} برای غرفه دار یافت نشد.")

            product_price = db_product.get("price")
            item_count = item['count']
            total_item_price = product_price * item_count
            share_company_cost = decimal.Decimal(total_item_price) * decimal.Decimal(vendor_share_rate)

            parcel_item_data = {
                'product_id': db_product.get('id'),
                'price': product_price,
                'count': item_count,
                'share_company': share_company_cost,
                'vendor_id': vendor_id,
            }

            sum_total_price.append(decimal.Decimal(total_item_price))
            sum_count_product.append(item_count)
            sum_share_company.append(share_company_cost)
            current_vendor_items.append(parcel_item_data)

            key_vendor = 'vendor_id'

            if key_vendor not in production:
                production[key_vendor] = vendor_id

            last_vendor_id = vendor_id

        if production.get('vendor_id') is not None:
            productionUpdate = {
                'customer_id': customer_id,
                'price': sum(sum_total_price),
                'count': sum(sum_count_product),
                'share_company': sum(sum_share_company),
                'invoice_id': get_invoice[0].id,
                'created_at': datetime.now(),
                'origin': customer_origin,
                'status': EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM,
                'delivery': EnumInvoice.STATUS_DELIVERY,
                'methodpost': EnumInvoice.METHOD_POST,
                'vendor_id': last_vendor_id
            }
            production.update(productionUpdate)
            productive.append(production)
            print(productive)
        get_parcel = await RepositoryParcel.get_parcel(vendor_id=[last_vendor_id], customer_id=customer_id)

        if not get_parcel or get_parcel[0].created_at < day_ago:
            create_parcels = await RepositoryParcel.create_return_many(productive)
            for parcel_data in create_parcels:
                for parcel_item in current_vendor_items:
                    if parcel_item.get('vendor_id') == parcel_data.vendor_id:
                        parcel_item['parcel_id'] = parcel_data.id

        create_parcelItem = await RepositoryItem.create_return_many(current_vendor_items)

        kafka_manager = kafka()
        await kafka_manager.start()
        await kafka_manager.produce(get_parcel)
        await kafka_manager.stop()
        return ProductParcelSchema(
            vendor_id=vendor_id_list,
            customer_id=customer_id,
            price=total_amount,
            count=total_item_count,
            share_company=int(total_share_company),
            invoice_id=get_invoice[0].id,
            created_at=datetime.now(),
            origin=customer_origin,
            status=EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM,
            delivery=EnumInvoice.STATUS_DELIVERY,
            methodpost=EnumInvoice.METHOD_POST
        )