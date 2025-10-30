import datetime
import decimal
from typing import Dict, Any, Set, Tuple,List
from fastapi import APIRouter,HTTPException,status,Query
from Enum.EnumInvoice import EnumInvoice
from hepler.helper_parcel import get_and_check_entity, get_item_and_product_details
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
        update =await RepositoryParcel.update_by_id(parcel_id , {'delivery':'ارسال شده توسط غرفه دار'})
        invoice_id = get_parcel[0].get('invoice_id')
        get_invoice = await get_and_check_entity(
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

        for index  in get_all_parcel[0:]:
          if (value == 'ارسال شده توسط غرفه دار' for value in index.values()):
              update_invoice =await  RepositoryInvoice.update_by_id(get_parcel[0].get('invoice_id'),{'delivery':'تمامی مرسوله های شما ارسال شده اند'})

        return {'message':'done'}

@router.get('/vendor/list_product/')
async def all_list_product():
    query =await RepositoryProduct.all()
    list_product= []
    for item in query :
        name_product=item.name
        price=item.price
        query_vendor = RepositoryVendor.select_where(RepositoryVendor.field('id').eq(item.vendor_id)).select('*')
        execute_vendor=await  RepositoryVendor.execute_and_fetch(query_vendor)
        name_vendor = execute_vendor[0].get('name')
        last_name = execute_vendor[0].get('last_name')
        show =ShowProductSchema(
        name_vendor=name_vendor,
        last_name_vendor=last_name,
        price=price,
        name=name_product,
        )
        list_product.append(show)
    return list_product



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
    print(execute)
    update =await RepositoryParcel.update_by_id(parcel_id, {'status':f'{sender}کنسل شده توسط '})
    execute_product = await get_item_and_product_details(parcel_id)
    print(execute_product)

    count= execute_product.get('count')
    price = execute_product.get('products').get('price')
    name = execute_product.get('products').get('name')
    print(price)
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
    print(execute)
    id_vendor = [id['id'] for id in execute]

    execute_parcel=await get_and_check_entity(
        RepositoryParcel,
        identifier=id_vendor,
        field_name='vendor_id',
        error_message='this vendor is not exist'
    )

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
    for value in execute_product:
        name_product = value['name']
        price_product = value['price']
        priceParcel = value['price']
        countParcel = execute_parcel[0].get('count')
        statusParcel=execute_parcel[0].get('status')
        originParcel = execute_parcel[0].get('origin')
        show = ShowParcel(
            id = id_parcelItem,
            TotalPrice =priceParcel,
            price = price_product,
            nameProduct = name_product,
            count = countParcel,
            status= statusParcel,
            origin = originParcel
        )
        list_product.append(show)
    return list_product

@router.post('/add_parcel/')
async def add_item_parcel(name:str,last_name:str,data:dict[str,dict[str,Any]]=CreateParcelSchema):
    get_customer =await get_and_check_entity(
        RepositoryCustomer,
        identifier=last_name,
        field_name='last_name'
    )
    get_invoice = await get_and_check_entity(
        RepositoryInvoice,
        identifier=get_customer[0].get('id'),
        field_name='customer_id',
    )
    value_invoice ={
        "customer_id":get_customer[0].get('id'),
        'status':EnumInvoice.INVOICE_AWAIT_FOR_CONFIRM,
    }
    if not get_invoice:
        get_invoice = await RepositoryInvoice.create_return(value_invoice)
    id_invoice= get_invoice[0].get('id')

    unique_vendor_keys: Set[Tuple[str, str]] = set()
    structured_data = {}

    for key, value in data.get('data').items():
        vendor_name, vendor_last_name = key.split('-', 1)
        unique_vendor_keys.add((vendor_name, vendor_last_name))
        structured_data[key] = value

    vendor_names = [v[0] for v in unique_vendor_keys]
    vendor_last_names = [v[1] for v in unique_vendor_keys]
    query_vendors = await RepositoryVendor.get_vendor(vendor_names, vendor_last_names)
    totalPrice = []
    countProduct = []
    vendor_id_list = [value.id for value in query_vendors]
    share_company_parcel=[]
    nameProduct = []
    current_parcelItem_data={}
    productive = []
    parceItem=[]
    for vendor_key, products_list in structured_data.items():

        vendor_name = vendor_key.split('-')[0]
        vendor_last_name = vendor_key.split('-')[1]
        vendor_id = await get_and_check_entity(
            RepositoryVendor,
            identifier=vendor_name,
            field_name='name',
            last_name=vendor_last_name
        )
        for item in products_list:
            counter = 0


            nameProduct.append(item['product_name'])
            countProduct.append(item['count'])
            share_company_parcel.append((int(item['count'])*int(item['price']))*vendor_id[0].get('share') )
            totalPrice.append(int(item['count'])* int(item['price']) )
            product = await get_and_check_entity(
                RepositoryProduct,
                identifier=nameProduct,
                field_name='name',
            )
            current_parcelItem_data = {
                    i: {
                        'product_id': product[i]['id'],
                        'price': product[i]['price'],
                        'count': item['count'],
                        'share_company': int((item['count'])*int(item['price']))*vendor_id[0].get('share'),
                        'vendor_id': vendor_id[0].get('id'),
                    }
                    for i in range(0,len(nameProduct))

                }

        production = {
            'vendor_id': vendor_id[0].get('id'),
            'customer_id': get_customer[0].get('id'),
            'price': sum(totalPrice),
            'count': sum(countProduct),
            'share_company': decimal.Decimal(sum(share_company_parcel)),
            'invoice_id': id_invoice,
            'created_at': datetime.datetime.now(), 'origin': get_customer[0].get('city'),
            'status': EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM, 'delivery': EnumInvoice.STATUS_DELIVERY,
            'methodpost': EnumInvoice.METHOD_POST}
        productive.append(production)

        totalPrice=[]
        countProduct=[]
        share_company_parcel=[]

        get_parcel = await RepositoryParcel.get_parcel(vendor_id=[vendor_id[0].get('id')],customer_id=get_customer[0].get('id'))
        if not get_parcel:

            create_parcels = await RepositoryParcel.create_return_many(productive)
            new_parcel_id = create_parcels[0].get('id')

            for item_index in current_parcelItem_data:
                current_parcelItem_data[item_index]['parcel_id'] = new_parcel_id
            parceItem.append(current_parcelItem_data)
            get_parcel = create_parcels
        else:
            existing_parcel = get_parcel[0]
            existing_parcel_id = existing_parcel.id

            new_parcel_items_for_db = []
            for item_data in current_parcelItem_data.values():
                 if existing_parcel.vendor_id== item_data.get('vendor_id'):
                    item_data['parcel_id'] = existing_parcel_id
                    new_parcel_items_for_db.append(item_data)
            await RepositoryItem.create_return_many(new_parcel_items_for_db)
        counter += 1



    count=0
    parcel={}



    unique_record_key = str(count)
    count += 1

    print(current_parcelItem_data)
    amir = [ recordParcelItem for recordParcelItem in current_parcelItem_data.values() ]
    createProduct =await RepositoryItem.create_return_many(amir)
    print(amir)
    return ProductParcelSchema(
            vendor_id = vendor_id_list ,
            customer_id=get_customer[0].get('id'),
            price = sum(totalPrice),
            count = sum(countProduct),
            share_company=int(sum(share_company_parcel)),
            invoice_id=id_invoice,
            created_at=datetime.datetime.now(),
            origin=get_customer[0].get('city'),
            status = EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM,
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
async def add_confirm(parcel_id: List[int] = Query(alias="parcel_id",description='list of parcel id for confirm')) :
        query_parcel = await get_and_check_entity(
            RepositoryParcel ,
            identifier=parcel_id,
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
        print(item.balance)
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



