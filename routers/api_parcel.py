import datetime
import decimal
# from http.client import HTTPException
from traceback import print_tb

from fastapi import APIRouter,HTTPException

from repository.Customer import RepositoryCustomer
from repository.Invoice import RepositoryInvoice
from repository.Vendor import RepositoryVendor
from repository.parcelRepo import RepositoryParcel
from repository.parcelItem import RepositoryItem
from repository.product import RepositoryProduct
from schema.SchemShowProduct import ShowProductSchema
from schema.SchemaParcel import CreateParcelSchema
from schema.SchemaShowInvoice import ShowInvoice
from schema.SchemaShowParcel import ShowParcel

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
        query_parcel = RepositoryParcel.select_where(RepositoryParcel.field('id').eq(parcel_id)).select('*')
        execute_parcel =await RepositoryParcel.execute_and_fetch(query_parcel)
        if not execute_parcel:
            raise HTTPException(status_code=404, detail="this parcel is not exist")
        update =await RepositoryParcel.update_by_id(parcel_id , {'delivery':'ارسال شده توسط غرفه دار'})
        invoice_id = execute_parcel[0].get('invoice_id')
        query_invoice = RepositoryInvoice.select_where(RepositoryInvoice.field('id').eq(invoice_id)).select('*')
        execute_invoice = await RepositoryInvoice.execute_and_fetch(query_invoice)
        if not execute_invoice:
            raise HTTPException(status_code=404, detail="this invoice is not exist")
        query_all_parcel = RepositoryParcel.select_where(RepositoryParcel.field('invoice_id').eq(invoice_id)).select('*')
        execute_all_parcel =await RepositoryParcel.execute_and_fetch(query_all_parcel)
        dictParcel = execute_all_parcel
        # print(dictParcel[0:])
        for index  in dictParcel[0:]:
          if (value == 'ارسال شده توسط غرفه دار' for value in index.values()):
              update_invoice =await  RepositoryInvoice.update_by_id(execute_parcel[0].get('invoice_id'),{'delivery':'تمامی مرسوله های شما ارسال شده اند'})

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



@router.get('/invoice/{customer_id}')
async def get_parcel_for_customer(customer_id: int):

    query = RepositoryInvoice.select_where(RepositoryInvoice.field('customer_id') == customer_id).select('id')
    execute =await RepositoryInvoice.execute_and_fetch(query)
    invoice_id = execute[0].get('id')
    query_parcel= RepositoryParcel.select_where(RepositoryParcel.field('invoice_id').eq(invoice_id)).select('*')
    execute_parcel =await RepositoryParcel.execute_and_fetch(query_parcel)
    show_list=[]
    for item in execute_parcel:
        saveParcelId = item['id']
        saveTotalPrice = item['price']
        getParcelItem = RepositoryItem.select_where(RepositoryItem.field('parcel_id').eq(saveParcelId)).select('*')
        execute_item =await RepositoryItem.execute_and_fetch(getParcelItem)
        count = execute_item[0].get('count')
        get_product = RepositoryProduct.select_where(RepositoryProduct.field('id').eq(execute_item[0].get('product_id'))).select('*')
        execute_item =await RepositoryProduct.execute_and_fetch(get_product)
        name = execute_item[0].get('name')
        price = decimal.Decimal(execute_item[0].get('price'))
        show = ShowParcel(
            id_parcel= saveParcelId,
            TotalPrice=saveTotalPrice,
            price=price,
            nameProduct=name,
            count=count,
            status=execute_parcel[0].get('status')
        )
        show_list.append(show)

    print(show_list)
    return show_list


@router.get('/parcel/{parcel_id}',response_model=ShowParcel)
async def cancel_one_parcel(parcel_id: int):
    get_parcel = RepositoryParcel.select_where(RepositoryParcel.field('id').eq(parcel_id)).select('*')
    execute =await RepositoryParcel.execute_and_fetch(get_parcel)
    if not execute :
        raise Exception('parcel is not exist')

    update =await RepositoryParcel.update_by_id(parcel_id, {'status': 'cancel'})
    query_item = RepositoryItem.select_where(RepositoryItem.field('parcel_id').eq(parcel_id)).select('*')
    execute_item =await RepositoryItem.execute_and_fetch(query_item)
    count = execute_item[0].get('count')
    product_id =execute_item[0].get('product_id')
    query_product = RepositoryProduct.select_where(RepositoryProduct.field('id').eq(product_id)).select('*')
    execute_product = await RepositoryProduct.execute_and_fetch(query_product)


    price = execute_product[0].get('price')
    name = execute_product[0].get('name')

    return  ShowParcel(
        id= parcel_id,
        TotalPrice=execute[0].get('price') ,
        price=price,
        nameProduct=name ,
        count=count,
        status=execute[0].get('status'),

    )
@router.get('/parcel/{user_id}')
async def get_parcel_for_vendor(user_id:int):
    # تعداد کل محصولات یک سفارش و اسم سفارش قیمت کل سفارش مقصد هر سفارش
    query = RepositoryParcel.select_where(RepositoryParcel.field('vendor_id').eq(user_id)).select('*')
    execute=await RepositoryParcel.get(query,relations=['invoice'])
    for item in execute:
        query_item= RepositoryItem.select_where(RepositoryItem.field('parcel_id').eq(item.id)).select('*')
    #پیدا کردن آیتم های سفارش بر اساس شماره سفارش
        execute_item= await RepositoryItem.execute_and_fetch(query_item)

    #گرفتن محصول
        query_product = RepositoryProduct.select_where(RepositoryProduct.field('id').eq(execute_item[0].get('product_id'))).select('*')
        execute_product = await RepositoryProduct.execute_and_fetch(query_product)
        name_product = execute_product[0].get('name')
        price_product = execute_product[0].get('price')
        print(name_product)


@router.post('/add_parcel/')
async def add_item_parcel(data:CreateParcelSchema):
    query_origin_customer = RepositoryCustomer.select_where(RepositoryCustomer.field('name').eq(data.customer_name.get('name'))).where(RepositoryCustomer.field('last_name').eq(data.customer_name.get('last_name'))).select('*')
    execute_customer = await RepositoryCustomer.execute_and_fetch(query_origin_customer)
    if not execute_customer :
        raise HTTPException(status_code=404,detail='customer is not exist')

    query_vendor =f'''
    (select * from vendor where name='{data.vendor_name}' and last_name = '{data.last_name_vendor}') 
    '''
    execute_vendor = await RepositoryVendor.execute_and_fetch(query_vendor)

    if not execute_vendor:
        raise HTTPException(status_code=404,detail='vendor is not exist')

    value_invoice = {
        'customer_id': execute_customer[0].get('id'),
        'status': 'در انتظار ثبت خرید',
        'vendor_id': execute_vendor[0].get('id'),
        'origin': execute_customer[0].get('origin'),
        'create_at': datetime.datetime.now(),
        'update_at': datetime.datetime.now(),
    }

    existing_invoice_query = RepositoryInvoice.select_where(
        RepositoryInvoice.field('customer_id').eq(value_invoice['customer_id'])
    ).select('*')
    existing_invoice = await RepositoryInvoice.execute_and_fetch(existing_invoice_query)

    if not existing_invoice:
        new_invoice = await RepositoryInvoice.create_return(value_invoice)
        order = [new_invoice]

    else:
        order = existing_invoice
    get_item = await RepositoryProduct.execute_and_fetch(
        RepositoryProduct.select_where(RepositoryProduct.field('name').eq(data.product_id)).select('*'))
    if not get_item :
        raise HTTPException(status_code=404,detail='product is not exist')
    price = (data.count) * (get_item[0].get('price'))
    vendor_id = execute_vendor[0].get('share')
    share_company = round((price * vendor_id) / 100)

    value_parcel = {
        'vendor_id':execute_vendor[0].get('id'),
        'customer_id': execute_customer[0].get('id'),
        'price':price ,
        'share_company':share_company,
        'invoice_id':order[0].get('id'),
        'count': data.count,
        'status':'در انتظار ثبت خرید' ,
        'origin':execute_customer[0].get('origin'),

    }
    query_parcel= (RepositoryParcel.select_where(RepositoryParcel.field('invoice_id').eq(order[0].get('id'))).select('*'))
    execute_parcel =await RepositoryParcel.execute_and_fetch(query_parcel)

    if  not execute_parcel :
        parcel =await RepositoryParcel.create_return(value_parcel)
        parcel_id = parcel.id
        print(parcel_id)
    else:
        parcel =await RepositoryParcel.execute_and_fetch(RepositoryParcel.select_where(RepositoryParcel.field('invoice_id').eq(order[0].get('id'))).select('*'))
        parcel_id = parcel[0].get('id')
    value_parcelItem = {
        'parcel_id' : parcel_id,
        'product_id':get_item[0].get('id'),
        'count': data.count,
        'price': price,
        'share_company': share_company,
    }
    if not (await RepositoryItem.execute_and_fetch(RepositoryItem.select_where(RepositoryItem.field('parcel_id').eq(value_parcelItem['parcel_id'])).where(RepositoryItem.field('product_id').eq(data.product_id))) ):
        parcelItem =await RepositoryItem.create_return(value_parcelItem)
    return ShowInvoice(
        id=order[0].get('id'),
        customer_id=execute_customer[0].get('id'),
        status=value_invoice['status'],
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )





@router.get('/submit/{invoice_id}')
async def add_confirm(invoice_id:int) :

    query = RepositoryInvoice.select_where(RepositoryInvoice.field('id').eq(invoice_id)).select('*')
    get_invoice =await RepositoryInvoice.execute_and_fetch(query)
    if get_invoice:
        await RepositoryInvoice.update_by_id(get_invoice[0].get('id'), {'status': 'تایید خرید'})
        parcel_query = RepositoryParcel.select_where(RepositoryParcel.field('invoice_id').eq(invoice_id)).select('*')

        parcel_execute =await RepositoryParcel.execute_and_fetch(parcel_query)
        for item in parcel_execute :
            await RepositoryParcel.update_by_id(item.get('id'),{'status': 'تایید خرید'})

    else:
        raise Exception('همچین شماره سفارشی موجود نمیباشد ')

@router.get('/cancel_invoice/{invoice_id}')
async def cancel_invoice(invoice_id:int):

    query = RepositoryInvoice.select_where(RepositoryInvoice.field('id').eq(invoice_id)).select('*')
    get_invoice =await RepositoryInvoice.execute_and_fetch(query)
    if get_invoice:
        await RepositoryInvoice.update_by_id(get_invoice[0].get('id'), {'status': 'کنسل شد '})
        parcel_query = RepositoryParcel.select_where(RepositoryParcel.field('invoice_id').eq(invoice_id)).select('*')

        parcel_execute =await RepositoryParcel.execute_and_fetch(parcel_query)
        for item in parcel_execute :
            await RepositoryParcel.update_by_id(item.get('id'),{'status': 'کنسل شد '})

    else:
        raise Exception('همچین شماره سفارشی موجود نمیباشد ')




@router.get('/set_share/{vendor_id}')
async def set_share(vendor_id:int,num: decimal.Decimal ):
    query_vendor= RepositoryVendor.select_where(RepositoryVendor.field('id').eq(vendor_id)).select('*')
    execute =await RepositoryVendor.execute_and_fetch(query_vendor)
    if not execute  :
        raise Exception('this vendor is not exist')

    if execute[0].get('share') != None:
            raise Exception('this vendor have share field')

    percent= num/100
    print(percent)
    update_share =await RepositoryVendor.update_by_id(vendor_id,{'share':percent})
    return  {'message': 'share with successfully submit'}
