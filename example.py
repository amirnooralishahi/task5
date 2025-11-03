import asyncio
import datetime
import decimal
from typing import Any, Dict, List, Set, Tuple
from app.enums import EnumInvoice
from app.schemas import ProductParcelSchema


async def calculate_vendor_totals(items: List[Dict[str, Any]], vendor_share: decimal.Decimal):
    """محاسبه جمع قیمت‌ها، تعداد و سهم شرکت برای هر فروشنده"""
    total_price = sum(int(i['count']) * int(i['price']) for i in items)
    total_count = sum(int(i['count']) for i in items)
    total_share = sum(decimal.Decimal(i['count']) * decimal.Decimal(i['price']) * vendor_share for i in items)
    return total_price, total_count, total_share


async def add_item_parcel(name: str, last_name: str, data: Dict[str, Any] = None):
    # 1️⃣ گرفتن اطلاعات مشتری
    get_customer = await get_and_check_entity(
        RepositoryCustomer,
        identifier=name,
        field_name='name',
        last_name=last_name
    )
    customer_id = get_customer[0]['id']
    customer_city = get_customer[0]['city']

    # 2️⃣ دریافت یا ساخت فاکتور
    get_invoice = await RepositoryInvoice.get_invoice(customer_id=customer_id)
    if not get_invoice:
        get_invoice = await RepositoryInvoice.create_return({
            'customer_id': customer_id,
            'status': EnumInvoice.INVOICE_AWAIT_FOR_CONFIRM,
        })
    invoice_id = get_invoice[0].id

    # 3️⃣ تجزیه داده‌ها
    structured_data = data.get('data', {})
    unique_vendor_keys: Set[Tuple[str, str]] = {tuple(k.split('-', 1)) for k in structured_data.keys()}

    # 4️⃣ هم‌زمان گرفتن اطلاعات تمام فروشنده‌ها
    vendor_tasks = [
        get_and_check_entity(RepositoryVendor, identifier=vn, field_name='name', last_name=vl)
        for vn, vl in unique_vendor_keys
    ]
    vendors_info_list = await asyncio.gather(*vendor_tasks)
    vendor_info_map = {f"{v[0]['name']}-{v[0]['last_name']}": v[0] for v in vendors_info_list}

    # 5️⃣ ساخت لیست تمام محصولات برای دریافت هم‌زمان
    product_tasks = []
    for vendor_key, products in structured_data.items():
        vendor_id = vendor_info_map[vendor_key]['id']
        for item in products:
            product_tasks.append(
                get_and_check_entity(
                    RepositoryProduct,
                    identifier=item['product_name'],
                    field_name='name',
                    vendor_id=vendor_id
                )
            )
    products_info_list = await asyncio.gather(*product_tasks)

    # map از نام محصول → اطلاعات محصول
    products_map = {p[0]['name']: p[0] for p in products_info_list}

    # 6️⃣ پردازش داده‌ها و ساخت مرسوله‌ها
    total_amount = 0
    total_item_count = 0
    total_share_company = decimal.Decimal(0)
    productive = []
    parcel_items = []

    for vendor_key, items in structured_data.items():
        vendor = vendor_info_map[vendor_key]
        vendor_id = vendor['id']
        vendor_share = vendor['share']

        price, count, share = await calculate_vendor_totals(items, vendor_share)

        production = {
            'vendor_id': vendor_id,
            'customer_id': customer_id,
            'price': price,
            'count': count,
            'share_company': share,
            'invoice_id': invoice_id,
            'created_at': datetime.datetime.now(),
            'origin': customer_city,
            'status': EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM,
            'delivery': EnumInvoice.STATUS_DELIVERY,
            'methodpost': EnumInvoice.METHOD_POST
        }
        productive.append(production)

        # ساخت آیتم‌ها
        parcel_items.extend([
            {
                'product_id': products_map[item['product_name']]['id'],
                'price': int(item['price']),
                'count': int(item['count']),
                'share_company': decimal.Decimal(item['price']) * decimal.Decimal(vendor_share),
                'vendor_id': vendor_id
            }
            for item in items
        ])

        total_amount += price
        total_item_count += count
        total_share_company += share

    # 7️⃣ ساخت یا آپدیت مرسوله‌ها و آیتم‌ها
    created_parcels = await RepositoryParcel.create_return_many(productive)
    for idx, parcel in enumerate(created_parcels):
        for item in parcel_items:
            if item['vendor_id'] == parcel.vendor_id:
                item['parcel_id'] = parcel.id

    await RepositoryItem.create_return_many(parcel_items)

    # 8️⃣ ارسال به Kafka
    kafka_manager = kafka()
    await kafka_manager.start()
    await kafka_manager.produce(created_parcels)
    await kafka_manager.stop()

    # ✅ خروجی نهایی
    return ProductParcelSchema(
        vendor_id=[v['id'] for v in vendor_info_map.values()],
        customer_id=customer_id,
        price=total_amount,
        count=total_item_count,
        share_company=int(total_share_company),
        invoice_id=invoice_id,
        created_at=datetime.datetime.now(),
        origin=customer_city,
        status=EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM,
        delivery=EnumInvoice.STATUS_DELIVERY,
        methodpost=EnumInvoice.METHOD_POST
    )
