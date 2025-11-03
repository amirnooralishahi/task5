import datetime
import decimal
from traceback import print_tb
from typing import Dict, Any, Set, Tuple, List, Union
from fastapi import APIRouter,HTTPException,status,Query
from decimal import Decimal
import kafkaProject.expirationParcel
from Enum.EnumInvoice import EnumInvoice
from hepler.helper_parcel import get_and_check_entity, get_item_and_product_details, check_and_buy_item
from repository.Customer import RepositoryCustomer
from repository.Invoice import RepositoryInvoice
from repository.Vendor import RepositoryVendor
from repository.parcelRepo import RepositoryParcel
from repository.parcelItem import RepositoryItem
from repository.product import RepositoryProduct
from schema.SchemShowProduct import ShowProductSchema
from schema.SchemaParcel import CreateParcelSchema, ProductParcelSchema
from schema.SchemaSendPostVendor import ShowPostVendor
from schema.SchemaShowParcel import ShowParcel, ShowCancelParcel, ShowCancelInvoice
from schema.SchemaVendor import ShowVendorSchema
from kafkaProject.expirationParcel import kafka
router = APIRouter(
    prefix='/parcel',
    tags=['parcel']
)

"جرنی کامل خرید"
"ارسال سفارش توسط هر فروشنده"
"نمایش جزییات خرید به مشتری"
"نمایش جزییاس سفارش برای هر فروشنده"
"امکان تنظیم کارمزد برای هر فروشنده توسط ادمین"

@router.get('send_product_to_customer/{parcel_id}')
async def send_product_to_customer(parcel_id:int ):
        get_parcel =await get_and_check_entity(
            RepositoryParcel,
            parcel_id,
            'id',
            'this parceel is not exist'
        )
        await RepositoryParcel.update_by_id(parcel_id , {'delivery':'ارسال شده توسط غرفه دار'})
        invoice_id = get_parcel[0].get('invoice_id')
        await get_and_check_entity(
            RepositoryInvoice,
            invoice_id,
            'id',
            'this invoice is not exist'
        )
        get_all_parcel =await get_and_check_entity(
            RepositoryParcel,
            invoice_id,
            'invoice_id'
        )
        value= [await  RepositoryInvoice.update_by_id(invoice_id,{'delivery':'تمامی مرسوله های شما ارسال شده اند'})
                for index in get_all_parcel
                for value in index.values() if value =='ارسال شده توسط غرفه دار']

        return {'message':'done'}

@router.get('/vendor/list_product/')
async def all_list_product():
   all_list =await RepositoryProduct.all()
   vendor_id = [value.vendor_id for value in all_list]
   name_product = [value.name for value in all_list]
   price = [value.price for value in all_list]
   print(all_list)
   get_vendor=  await RepositoryVendor.find_by_many_id(vendor_id)
   vendor = {
       value.id:{'name':value.name,'last_name':value.last_name}
       for value in get_vendor
   }
   listProduct = []
   for i in range(len(vendor_id)):
       for key , value in vendor.items():
           if vendor_id[i] == key :
               show= {i:{
                   'nameVendor': value['name'],
                   'lastNameVendor': value['last_name'],
                   'nameProduct': name_product[i],
                   'price': price[i],
               }}
               listProduct.append(show)

   print(listProduct)
   return  listProduct

@router.get('/parcel-customer/')
async def get_parcel_for_customer(name:str , last_name:str):
    query_customer =await get_and_check_entity(
        RepositoryCustomer,
        identifier=name,
        field_name='name' ,
        last_name=last_name
    )
    execute =await get_and_check_entity(
        RepositoryInvoice,
        identifier=query_customer[0].get('id'),
        field_name='customer_id',
    )
    invoice_id = execute[0].get('id')
    # RepositoryParcel.select_where(RepositoryParcel.field('invoice_id').eq(invoice_id)).select('*')
    execute_parcel =await get_and_check_entity(
        RepositoryParcel,
        identifier=invoice_id,
        field_name='invoice_id',
    )
    show_list=[]
    for item in execute_parcel:

            saveParcelId = item['id']
            execute_item =await get_and_check_entity(
                RepositoryItem,
                identifier=saveParcelId,
                field_name='parcel_id'
            )
            count = execute_item[0].get('count')
            get_product = RepositoryProduct.select_where(RepositoryProduct.field('id').eq(execute_item[0].get('product_id'))).select('*')
            execute_item =await RepositoryProduct.execute_and_fetch(get_product)
            name = execute_item[0].get('name')
            price = (execute_item[0].get('price'))
            show = ShowParcel(
                id= saveParcelId,
                TotalPrice=execute_parcel[0].get('price'),
                price=price,
                nameProduct=name,
                count=count,
                status=execute_parcel[0].get('status'),
                origin=execute_parcel[0].get('origin')
            )
            show_list.append(show)

    return show_list


@router.get('/parcel/',response_model=ShowCancelParcel)
async def cancel_one_parcel(parcel_id: int,name:str , last_name:str):
    query_customer=await RepositoryCustomer.get_customer(name,last_name)
    if query_customer:
        sender = 'مشتری'
    execute_vendor=await get_and_check_entity(
        RepositoryVendor,
        identifier=name ,
        field_name='name',
        last_name=last_name
    )
    execute =await get_and_check_entity(
        RepositoryParcel,
        identifier=parcel_id,

    )

    update =await RepositoryParcel.update_by_id(parcel_id, {'status':f'{sender}کنسل شده توسط '})
    execute_product = await get_item_and_product_details(parcel_id)

    count= execute_product.get('count')
    price = execute_product.get('products').get('price')
    name = execute_product.get('products').get('name')

    return  ShowCancelParcel(
        TotalPrice=execute.price ,
        price=price,
        nameProduct=name ,
        count=count,
        status=execute.status,
        origin=execute.origin,
        sender=sender
    )
@router.get('/parcel-vendor/')
async def get_parcelItem_for_vendor(name:str , last_name:str):
    execute= await get_and_check_entity(
        RepositoryVendor,
        identifier=name ,
        field_name='name',
        error_message='this vendor is not exist',
        last_name=last_name
    )
    id_vendor = [id['id'] for id in execute]
    execute_parcel=await get_and_check_entity(
        RepositoryParcel,
        identifier=id_vendor,
        field_name='vendor_id',
        error_message='this parcel is not exist'
    )
    print(execute_parcel)
    list_product= []
    id_parcelItem = [id['id'] for id in execute_parcel]
    count_parcel = [value['count'] for value in execute_parcel]
    execute_item = await get_and_check_entity(
        RepositoryItem,
        identifier=id_parcelItem,
        field_name='parcel_id',
    )

    id_product = [id['product_id'] for id in execute_item]
    execute_product = await get_and_check_entity(
        RepositoryProduct,
        identifier=id_product,

    )

    name_product=[value['name'] for value in execute_product]
    price_product=[value['price'] for value in execute_product]
    price_parcel=[value['price']for value in execute_parcel]
    count_parcel = [value['count']for value in execute_parcel]
    status_parcel = [value['status'] for value in execute_parcel]
    origin_parcel = [value['origin'] for value in execute_parcel]

    show = ShowParcel(
        id = id_parcelItem,
        TotalPrice =price_parcel,
        price = price_product,
        nameProduct = name_product,
        count = count_parcel,
        status= status_parcel,
        origin = origin_parcel
    )
    list_product.append(show)
    return show
# @router.post('/add_parcel/')
# async def add_item_parcel(name:str,last_name:str,data:dict[str,dict[str,Any]]=CreateParcelSchema):
#     get_customer =await get_and_check_entity(
#         RepositoryCustomer,
#         identifier=last_name,
#         field_name='last_name'
#     )
#     get_invoice = await get_and_check_entity(
#         RepositoryInvoice,
#         identifier=get_customer[0].get('id'),
#         field_name='customer_id',
#     )
#     value_invoice ={
#         "customer_id":get_customer[0].get('id'),
#         'status':EnumInvoice.INVOICE_AWAIT_FOR_CONFIRM,
#     }
#     if not get_invoice:
#         get_invoice = await RepositoryInvoice.create_return(value_invoice)
#     id_invoice= get_invoice[0].get('id')
#
#     unique_vendor_keys: Set[Tuple[str, str]] = set()
#     structured_data = {}
#
#     for key, value in data.get('data').items():
#         vendor_name, vendor_last_name = key.split('-', 1)
#         unique_vendor_keys.add((vendor_name, vendor_last_name))
#         structured_data[key] = value
#     amount=0
#     vendor_names = [v[0] for v in unique_vendor_keys]
#     vendor_last_names = [v[1] for v in unique_vendor_keys]
#     query_vendors = await RepositoryVendor.get_vendor(vendor_names, vendor_last_names)
#     totalPrice = []
#     countProduct = []
#     vendor_id_list = [value.id for value in query_vendors]
#     share_company_parcel=[]
#     nameProduct = []
#     current_parcelItem_data={}
#     productive = []
#     parceItem=[]
#     for vendor_key, products_list in structured_data.items():
#
#         vendor_name = vendor_key.split('-')[0]
#         vendor_last_name = vendor_key.split('-')[1]
#         vendor_id = await get_and_check_entity(
#             RepositoryVendor,
#             identifier=vendor_name,
#             field_name='name',
#             last_name=vendor_last_name
#         )
#         for item in products_list:
#             counter = 0
#
#
#             nameProduct.append(item['product_name'])
#             countProduct.append(item['count'])
#             share_company_parcel.append((int(item['count'])*int(item['price']))*vendor_id[0].get('share') )
#             totalPrice.append(int(item['count'])* int(item['price']) )
#             product = await get_and_check_entity(
#                 RepositoryProduct,
#                 identifier=nameProduct,
#                 field_name='name',
#             )
#             current_parcelItem_data = {
#                     i: {
#                         'product_id': product[i]['id'],
#                         'price': product[i]['price'],
#                         'count': item['count'],
#                         'share_company': int((item['count'])*int(item['price']))*vendor_id[0].get('share'),
#                         'vendor_id': vendor_id[0].get('id'),
#                     }
#                     for i in range(0,len(nameProduct))
#
#                 }
#
#
#         production = {
#             'vendor_id': vendor_id[0].get('id'),
#             'customer_id': get_customer[0].get('id'),
#             'price': sum(totalPrice),
#             'count': sum(countProduct),
#             'share_company': decimal.Decimal(sum(share_company_parcel)),
#             'invoice_id': id_invoice,
#             'created_at': datetime.datetime.now(), 'origin': get_customer[0].get('city'),
#             'status': EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM, 'delivery': EnumInvoice.STATUS_DELIVERY,
#             'methodpost': EnumInvoice.METHOD_POST}
#         productive.append(production)
#         amount+=sum(totalPrice)
#         totalPrice=[]
#         countProduct=[]
#         share_company_parcel=[]
#
#         get_parcel = await RepositoryParcel.get_parcel(vendor_id=[vendor_id[0].get('id')],customer_id=get_customer[0].get('id'))
#         if not get_parcel:
#
#             create_parcels = await RepositoryParcel.create_return_many(productive)
#             new_parcel_id = create_parcels[0].get('id')
#
#             for item_index in current_parcelItem_data:
#                 current_parcelItem_data[item_index]['parcel_id'] = new_parcel_id
#             parceItem.append(current_parcelItem_data)
#             get_parcel = create_parcels
#         else:
#             existing_parcel = get_parcel[0]
#             existing_parcel_id = existing_parcel.id
#
#             new_parcel_items_for_db = []
#             for item_data in current_parcelItem_data.values():
#                  if existing_parcel.vendor_id== item_data.get('vendor_id'):
#                     item_data['parcel_id'] = existing_parcel_id
#                     new_parcel_items_for_db.append(item_data)
#             await RepositoryItem.create_return_many(new_parcel_items_for_db)
#
#         counter += 1
#
#     # balance_customer = get_customer[0].get('balance')
#     # if balance_customer>amount :
#     #     balance_customer -=amount
#     #     await RepositoryCustomer.update_by_id(get_customer[0].get('id'),{'balance':balance_customer})
#     #
#     # else:
#     #     raise HTTPException(status_code=401, detail='balance is not enough')
#     count=0
#     parcel={}
#
#
#
#     unique_record_key = str(count)
#     count += 1
#
#
#     amir = [ recordParcelItem for recordParcelItem in current_parcelItem_data.values() ]
#     createProduct =await RepositoryItem.create_return_many(amir)
#     return ProductParcelSchema(
#             vendor_id = vendor_id_list ,
#             customer_id=get_customer[0].get('id'),
#             price = sum(totalPrice),
#             count = sum(countProduct),
#             share_company=int(sum(share_company_parcel)),
#             invoice_id=id_invoice,
#             created_at=datetime.datetime.now(),
#             origin=get_customer[0].get('city'),
#             status = EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM,
#             delivery=EnumInvoice.STATUS_DELIVERY,
#             methodpost=EnumInvoice.METHOD_POST
#     )
@router.post('/add_parcel/')
async def add_item_parcel(name: str, last_name: str, data: Dict[str, Dict[str, Any]] = CreateParcelSchema):

    get_customer = await get_and_check_entity(
        RepositoryCustomer,
        identifier=name,
        field_name='name',
        last_name=last_name
    )

    customer_id =get_customer[0].get('id')
    customer_origin=get_customer[0].get('origin')
    customer_balance = get_customer[0].get('balance')
    value_invoice = {
        'customer_id':customer_id,
        'status': EnumInvoice.INVOICE_AWAIT_FOR_CONFIRM,
    }

    get_invoice = await RepositoryInvoice.get_invoice(customer_id=customer_id)
    if not get_invoice:
        get_invoice = await RepositoryInvoice.create_return(value_invoice)
    structured_data = {}
    list_product = []
    for key, value in data.get('data').items():
        structured_data[key] = value
    for vendor , choice_product in structured_data.items():
        for item in choice_product:
            list_product.append({
                'vendor_name':item.get('vendorName'),
                'vendor_last_name':item.get('vendorLastName'),
                'nameProduct':item.get('nameProduct'),
                'price':item.get('price'),
                'count':item.get('count'),
            })


    total_amount = 0
    total_item_count = 0
    total_share_company = decimal.Decimal(0)
    current_parcelItem_data: List[Dict[str, Any]] = []
    productive: List[Dict[str, Any]] = []
    current_vendor_items: List[Dict[str, Any]] = []
    vendor_name=[key.split('-')[0] for key , value in structured_data.items()]
    vendor_last_name=[key.split('-')[1] for key , value in structured_data.items()]
    vendor_info = await get_and_check_entity(
        RepositoryVendor,
        identifier=vendor_name,
        field_name='name',
        last_name= vendor_last_name
    )
    vendor_share_map = {
        v.get('id'): v.get('share') for v in vendor_info
    }

    vendor_id_list=[value.get('id') for value in vendor_info]
    vendor_share_rate=[item['share'] for item in vendor_info]
    item_price = [int(item.get("price"))
                  for vendor, products_list in structured_data.items()
                  for item in products_list ]
    name_product = [value.get('product_name')
                    for vendor, products_list in structured_data.items()
                    for value in products_list]
    item_count = [int(item.get('count'))
                  for vendor, products_list in structured_data.items()
                  for item in products_list ]

    product = await get_and_check_entity(
        RepositoryProduct,
        identifier=name_product,
        field_name='name',
        vendor_id=vendor_id_list
    )
    product_map = {
        (p.get('name'), p.get('vendor_id')): p for p in product
    }
    product_total_price = [int(count) * int(price) for count, price in zip(item_count, item_price)]


    dictProduct ={'name': name_product,
                  'price': item_price,
                  'count': item_count }
    update=await check_and_buy_item(vendor_id_list,dictProduct,customer_id)
    if update !=status.HTTP_200_OK:
        raise HTTPException(status_code=406, detail='موجودی کافی نیست')
    current_vendor_items: List[Dict[str, Any]] = []

    for item in list_product:
        vendor_id = next(
            (v.get('id') for v in vendor_info if
             v.get('name') == item['vendor_name'] and v.get('last_name') == item['vendor_last_name']),
            None
        )
        print(list_product)

        if vendor_id is None:
            raise HTTPException(status_code=400, detail=f"غرفه دار {item['vendor_name']} یافت نشد.")

        vendor_share_rate = vendor_share_map.get(vendor_id, 0)  # نرخ سهم غرفه دار

        product_key = (item['product_name'], vendor_id)
        db_product = product_map.get(product_key)

        if not db_product:
            raise HTTPException(status_code=400, detail=f"محصول {item['product_name']} برای غرفه دار یافت نشد.")

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

        current_vendor_items.append(parcel_item_data)
        total_amount += total_item_price
        total_item_count += item_count
        total_share_company += share_company_cost    #

    production = {
        'vendor_id': vendor_id,
        'customer_id': customer_id,
        'price': total_amount,
        'count':total_item_count,
        'share_company': total_share_company,
        'invoice_id': get_invoice[0].id,
        'created_at': datetime.datetime.now(),
        'origin':  customer_origin,
        'status': EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM,
        'delivery': EnumInvoice.STATUS_DELIVERY,
        'methodpost': EnumInvoice.METHOD_POST
    }
    productive.append(production)
    get_parcel = await RepositoryParcel.get_parcel(vendor_id=[vendor_id], customer_id=customer_id)
    print(get_parcel)
    if not get_parcel:
        create_parcels = await RepositoryParcel.create_return_many(productive)
        new_parcel_id = create_parcels[0].id
        for item_data in current_vendor_items:
            item_data['parcel_id'] = new_parcel_id
            current_parcelItem_data.append(item_data)

        get_parcel = create_parcels
    else:
        existing_parcel_id = get_parcel[0].id

        for item_data in current_vendor_items:
            item_data['parcel_id'] = existing_parcel_id
        await RepositoryItem.create_return_many(current_vendor_items)
    kafka_manager = kafka()
    await kafka_manager.start()
    await kafka_manager.produce(get_parcel)
    await kafka_manager.stop()
    createProduct = await RepositoryItem.create_return_many(current_parcelItem_data)



    return ProductParcelSchema(
        vendor_id=vendor_id_list,
        customer_id= customer_id,
        price=total_amount,
        count=total_item_count,
        share_company=int(total_share_company),
        invoice_id=get_invoice[0].id,
        created_at=datetime.datetime.now(),
        origin= customer_origin,
        status=EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM,
        delivery=EnumInvoice.STATUS_DELIVERY,
        methodpost=EnumInvoice.METHOD_POST
    )

@router.get('/cancel_invoice/',response_model=ShowCancelInvoice)
async def cancel_invoice(invoice_id:int,name:str ,last_name:str):
    execute_customer=await get_and_check_entity(
        RepositoryCustomer,
        identifier=name,
        field_name='name',
        last_name=last_name
    )
    query =await get_and_check_entity(
        RepositoryInvoice ,
        identifier=invoice_id,
        field_name='id',
    )
    if execute_customer[0].get('id') != query.customer_id:
        raise HTTPException(status_code=405 , detail='this invoice not for you')
    parcel_query = await get_and_check_entity(
        RepositoryParcel,
        identifier=invoice_id,
        field_name='invoice_id'
    )
    if query:
        await RepositoryInvoice.update_by_id(query.id, {'status':EnumInvoice.INVOICE_CANCEL})
        for item in parcel_query :
            await RepositoryParcel.update_by_id(item.get('id'),{'status':EnumInvoice.PARCEL_CANCEL})
        return  ShowCancelInvoice(
            invoice_id=invoice_id,
            customer_name=execute_customer[0].get('name'),
            status=query.status,
        )


@router.get('/submit/')
async def add_confirm(parcel_id: Union[List[str],str] = Query(alias="parcel_id",description='list of parcel id for confirm')) :
    if isinstance(parcel_id, str):
        parcel_ids = [int(p.strip()) for p in parcel_id.split(',') if p.strip().isdigit()]
    elif isinstance(parcel_id, list):
        parcel_ids = []
        for p in parcel_id:
            if isinstance(p, str) and ',' in p:
                parcel_ids.extend([int(x.strip()) for x in p.split(',') if x.strip().isdigit()])

            elif str(p).isdigit():
                parcel_ids.append(int(p))
    else:
        parcel_ids = []

    query_parcel = await get_and_check_entity(
        RepositoryParcel ,
        identifier=parcel_ids,
    )

    if query_parcel[0].get('status') == EnumInvoice.PARCEL_CONFIRM_BY_VENDOR:
        raise HTTPException(status_code=422,detail='this parcel already submitted')

    change_status=await RepositoryParcel.update_by_id(query_parcel[0].get('id'),{'status':EnumInvoice.PARCEL_CONFIRM_BY_VENDOR})
    return  {'message':'with successfully confer'}




@router.get('/set_share/')
async def set_share(vendor_id:int,num: int ):
    query_vendor=await get_and_check_entity(
        RepositoryVendor,
        identifier=vendor_id,
    )


    percent = num / 100
    name = {query_vendor.name}
    last_name = {query_vendor.last_name}
    if query_vendor.share != None:
            update_share=RepositoryVendor.update_by_id(vendor_id,{'share':query_vendor.share})
            return {'message': f'share {percent} with successfully updated for {name}{last_name} '}

    update_share = await RepositoryVendor.update_by_id(vendor_id, {'share': percent})
    return  {'message': f'share {percent} with successfully submit for {name} {last_name} '}

@router.get('/list_vendor/')
async def list_vendor():
    execute =await  RepositoryVendor.all()
    vendor_list = []

    for item in execute :
        show=ShowVendorSchema(
            id = item.id,
            name = item.name,
            last_name = item.last_name ,
            phone = item.phone,
            balance=item.balance,

        )
        vendor_list.append(show)
    return  vendor_list


@router.get('/post_vendor/',response_model=ShowPostVendor)
async def post_parcel_vendor(name:str,last_name:str):

    execute =await get_and_check_entity(
        RepositoryVendor,
        identifier=name ,
        field_name='name',
        last_name=last_name
    )
    constFinally = 0

    execute_parcel = await get_and_check_entity(
        RepositoryParcel,
        identifier=execute[0].get('id'),
        field_name='vendor_id'
    )



    id_invoice =[value.get('invoice_id')  for value in execute_parcel]
    execute_parcel_all = await  get_and_check_entity(
        RepositoryParcel,
        identifier=id_invoice,
        field_name='invoice_id'
    )

    priceDelivery = [constFinally + value.get('pricedelivery') for value in execute_parcel_all if value.get('pricedelivery') is not None]
    DeliveryStatus = [value.get('delivery') for value in execute_parcel_all if value.get('delivery')=='مرسوله توسط غرفه دار ارسال شد ']
    id_parcel = [value.get('id') for value in execute_parcel]
    for id in id_parcel:
        update =await RepositoryParcel.update_by_id(id,{'delivery':EnumInvoice.PARCEL_SEND_BY_VENDOR,'pricedelivery':30000})

    customer_id = [value.get('customer_id') for value in execute_parcel]
    query_customer =await get_and_check_entity(
        RepositoryCustomer,
        identifier=customer_id,
    )
    name_customer = [value.get('name') for value in query_customer]
    last_name_customer =[value.get('last_name') for value in query_customer]
    id_vendor = [value.get('id') for value in execute]
    return ShowPostVendor(
            price_delivery=priceDelivery,
            parcel_id=id_parcel,
            name_customer=name_customer,
            lastName_customer=last_name_customer,
            statusDelivery=DeliveryStatus
        )






@router.get('/check_parcel_expire/')
async def check_parcel_expire(time,parcel_id=Union[List[int],int]):
    if isinstance(parcel_id, str):
        parcel_ids = [int(p.strip()) for p in parcel_id.split(',') if p.strip().isdigit()]
    elif isinstance(parcel_id, list):
        parcel_ids = []
        for p in parcel_id:
            if isinstance(p, str) and ',' in p:
                parcel_ids.extend([int(x.strip()) for x in p.split(',') if x.strip().isdigit()])

            elif str(p).isdigit():
                parcel_ids.append(int(p))
    else:
        parcel_ids = []

    execute =await get_and_check_entity(
        RepositoryParcel,
        identifier=parcel_ids,
        field_name='id',
    )
    kafka_manager =kafka()
    await kafka_manager.consumer(time,execute)
    return {'message':'with successfully set time'}

@router.post('/add-product-by-vendor/')
async def add_product_by_vendor(name:str,last_name:str, data: Dict[str, Any]):
    get_vendor=await get_and_check_entity(
        RepositoryVendor ,
        identifier=name,
        field_name='name',
        last_name=last_name
    )
    valueProduct = {
        'vendor_id':get_vendor[0].get("id"),
        'name':data.get('parcel').get('nameProduct'),
        'count':int(data.get('parcel').get('number')),
        'price':int(data.get('parcel').get('price')),
        'created_at':datetime.datetime.now(),
    }
    addProduct = await RepositoryProduct.create_return(valueProduct)
