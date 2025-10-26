import datetime
import decimal
# from http.client import HTTPException
from traceback import print_tb
from typing import List, Dict, Any
from functools import reduce
from fastapi import APIRouter,HTTPException,status

from repository.Customer import RepositoryCustomer
from repository.Invoice import RepositoryInvoice
from repository.Vendor import RepositoryVendor
from repository.parcelRepo import RepositoryParcel
from repository.parcelItem import RepositoryItem
from repository.product import RepositoryProduct
from schema.SchemShowProduct import ShowProductSchema
from schema.SchemaParcel import CreateParcelSchema
from schema.SchemaSendPostVendor import ShowPostVendor
from schema.SchemaShowInvoice import ShowInvoice
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



@router.get('/parcel-customer/')
async def get_parcel_for_customer(name:str , last_name:str):
    print(name , last_name)
    query_customer = RepositoryCustomer.select_where(RepositoryCustomer.field('name').eq(name)).select('*')
    execute_customer = await RepositoryCustomer.execute_and_fetch(query_customer)
    query = RepositoryInvoice.select_where(RepositoryInvoice.field('customer_id') == execute_customer[0].get('id')).select('id')
    execute =await RepositoryInvoice.execute_and_fetch(query)
    invoice_id = execute[0].get('id')
    query_parcel= RepositoryParcel.select_where(RepositoryParcel.field('invoice_id').eq(invoice_id)).select('*')
    execute_parcel =await RepositoryParcel.execute_and_fetch(query_parcel)
    print(execute_parcel)

    show_list=[]
    for item in execute_parcel:
        saveParcelId = item['id']
        getParcelItem = RepositoryItem.select_where(RepositoryItem.field('id').eq(saveParcelId)).select('*')
        execute_item =await RepositoryItem.execute_and_fetch(getParcelItem)
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

    print(show_list)
    return show_list


@router.get('/parcel/',response_model=ShowCancelParcel)
async def cancel_one_parcel(parcel_id: int,name:str , last_name:str):
    # print(parcel_id, name, last_name)
    query_customer= RepositoryCustomer.select_where(RepositoryCustomer.field('name') == name).where(RepositoryCustomer.field('last_name') == last_name).select('*')
    execute=await RepositoryCustomer.execute_and_fetch(query_customer)
    if execute:
        sender = 'مشتری'
    query_vendor = RepositoryVendor.select_where(RepositoryVendor.field('name').eq(name)).where(RepositoryVendor.field('last_name').eq(last_name)).select('*')
    execute_vendor=await RepositoryVendor.execute_and_fetch(query_vendor)
    if execute_vendor:
        sender= 'غرفه دار'
    get_parcel = RepositoryParcel.select_where(RepositoryParcel.field('id').eq(parcel_id)).select('*')
    execute =await RepositoryParcel.execute_and_fetch(get_parcel)
    if not execute :
        raise Exception('parcel is not exist')

    update =await RepositoryParcel.update_by_id(parcel_id, {'status':f'{sender}کنسل شده توسط '})
    query_item = RepositoryItem.select_where(RepositoryItem.field('parcel_id').eq(parcel_id)).select('*')
    execute_item =await RepositoryItem.execute_and_fetch(query_item)

    count = execute_item[0].get('count')
    product_id =execute_item[0].get('product_id')
    query_product = RepositoryProduct.select_where(RepositoryProduct.field('id').eq(product_id)).select('*')
    execute_product = await RepositoryProduct.execute_and_fetch(query_product)


    price = execute_product[0].get('price')
    name = execute_product[0].get('name')

    return  ShowCancelParcel(

        TotalPrice=execute[0].get('price') ,
        price=price,
        nameProduct=name ,
        count=count,
        status=execute[0].get('status'),
        origin=execute[0].get('origin'),
        sender=sender
    )
@router.get('/parcel-vendor/')
async def get_parcelItem_for_vendor(name:str , last_name:str):
    query_vendor=RepositoryVendor.select_where(RepositoryVendor.field('name').eq(name)).where(RepositoryVendor.field('last_name').eq(last_name)).select('*')
    execute= await RepositoryVendor.execute_and_fetch(query_vendor)
    # تعداد کل محصولات یک سفارش و اسم سفارش قیمت کل سفارش مقصد هر سفارش
    query = RepositoryParcel.select_where(RepositoryParcel.field('vendor_id').eq(execute[0].get('id'))).select('*')
    execute_parcel=await RepositoryParcel.execute_and_fetch(query)
    list_product= []
    for item in execute_parcel :
        query_item= RepositoryItem.select_where(RepositoryItem.field('parcel_id').eq(item.get('id'))).select('*')
        execute_item = await RepositoryItem.execute_and_fetch(query_item)
        if not execute_item:
            continue

        print(execute_item)
        for i in execute_item:
            query_product = RepositoryProduct.select_where(
                RepositoryProduct.field('id').eq(i.get('product_id'))).select('*')
            execute_product = await RepositoryProduct.execute_and_fetch(query_product)
            name_product = execute_product[0].get('name')
            price_product = execute_product[0].get('price')
            print(name_product)
            show = ShowParcel(
                id = item.get('id'),
                TotalPrice = item.get('price'),
                price = price_product,
                nameProduct = name_product,
                count = i.get('count'),
                status= item.get('status'),
                origin = item.get('origin')

            )
            list_product.append(show)
    return list_product

@router.post('/add_parcel/')
async def add_item_parcel(name:str,last_name:str,data:dict[str,dict[str,dict[str,Any]]]=CreateParcelSchema):
    query_origin_customer = RepositoryCustomer.select_where(RepositoryCustomer.field('name').eq(name)).where(RepositoryCustomer.field('last_name').eq(last_name)).select('*')
    share_company_parcel=0
    share_company = {}

    for item in data.get('data'):
        get_data = data.get('data').get(item).get('products')
        execute_customer = await RepositoryCustomer.execute_and_fetch(query_origin_customer)
        if not execute_customer :
            raise HTTPException(status_code=404,detail='customer is not exist')

        query_vendor =RepositoryVendor.select_where(RepositoryVendor.field('name').eq(get_data.get('nameVendor'))).where(RepositoryVendor.field('last_name').eq(get_data.get('last_nameVendor'))).select('*')
        execute_vendor = await RepositoryVendor.execute_and_fetch(query_vendor)
        if not execute_vendor:
            raise HTTPException(status_code=404,detail='vendor is not exist')

        value_invoice = {
            'customer_id': execute_customer[0].get('id'),
            'status': 'در انتظار ثبت خرید',
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
            order = new_invoice.id
        else:
            order = existing_invoice[0].get('id')
        query_product = RepositoryProduct.select_where(RepositoryProduct.field('name').eq(get_data.get('nameProduct'))).where(RepositoryProduct.field('vendor_id').eq(execute_vendor[0].get('id'))).select('*')
        get_item=await RepositoryProduct.execute_and_fetch(query_product)
        if not get_item :
            raise HTTPException(status_code=404,detail='product is not exist')
        price = (get_data.get('count_product')) * (get_item[0].get('price'))
        vendor_id_share = execute_vendor[0].get('share')
        share_company[execute_vendor[0].get('id')] =int(round((price * vendor_id_share)))

        share_company_parcelItem= int(round((price * vendor_id_share)))
        value_parcel = {
            'vendor_id':execute_vendor[0].get('id'),
            'customer_id': execute_customer[0].get('id'),
            'price':price ,
            'share_company':share_company[execute_vendor[0].get('id')],
            'invoice_id':order,
            'count': get_data.get('count_product'),
            'status':'در انتظار ثبت خرید' ,
            'origin':execute_customer[0].get('city'),
            'delivery':'در انتظار تایید غرفه دار '
        }
        print(value_parcel)
        query_parcel_vendor= RepositoryParcel.select_where(RepositoryParcel.field('vendor_id').eq(execute_vendor[0].get('id'))).where(RepositoryParcel.field(
            'invoice_id').eq(order)).select('*')
        execute_parcel_vendor=await RepositoryParcel.execute_and_fetch(query_parcel_vendor)
        if  not execute_parcel_vendor:
            parcel =await RepositoryParcel.create_return(value_parcel)
            parcel_id = parcel.id

        else:
            parcel =await RepositoryParcel.execute_and_fetch(RepositoryParcel.select_where(RepositoryParcel.field('invoice_id').eq(order)).select('*'))
            parcel_id = parcel[0].get('id')


        value_parcelItem = {
            'parcel_id' : parcel_id,
            'product_id':get_item[0].get('id'),
            'count':get_data.get('count_product'),
            'price':price ,
            'share_company': share_company_parcelItem,
        }

        if not (await RepositoryItem.execute_and_fetch(RepositoryItem.select_where(RepositoryItem.field('parcel_id').eq(value_parcelItem['parcel_id'])).where(RepositoryItem.field('product_id').eq(get_data.get('productName')))) ):
            parcelItem =await RepositoryItem.create_return(value_parcelItem)
    return ShowInvoice(
        id=order,
        customer_id=execute_customer[0].get('id'),
        status=value_invoice['status'],
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )



from fastapi import Query

@router.get('/submit/')
async def add_confirm(parcel_id: List[int] = Query(alias="parcel_id",description='list of parcel id for confirm')) :
        for item in parcel_id:
            query_parcel = RepositoryParcel.select_where(RepositoryParcel.field('id').eq(item)).select('*')
            execute_parcel = await RepositoryParcel.execute_and_fetch(query_parcel)
            if not execute_parcel :
                raise HTTPException(status_code=404,detail='parcel is not exist')
            change_status=await RepositoryParcel.update_by_id(execute_parcel[0].get('id'),{'status':'تایید شده توسط غرفه دار'})


@router.get('/cancel_invoice/',response_model=ShowCancelInvoice)
async def cancel_invoice(invoice_id:int,name:str ,last_name:str):
    query_customer=RepositoryCustomer.select_where(RepositoryCustomer.field('name').eq(name)).where(RepositoryCustomer.field('last_name').eq(last_name)).select('*')
    execute_customer=await RepositoryCustomer.execute_and_fetch(query_customer)
    if not execute_customer :
        raise HTTPException(status_code=404,detail='customer is not exist')

    query = RepositoryInvoice.select_where(RepositoryInvoice.field('id').eq(invoice_id)).select('*')
    get_invoice =await RepositoryInvoice.execute_and_fetch(query)
    if get_invoice:
        await RepositoryInvoice.update_by_id(get_invoice[0].get('id'), {'status': 'کل سفارش کنسل شد '})
        parcel_query = RepositoryParcel.select_where(RepositoryParcel.field('invoice_id').eq(invoice_id)).select('*')

        parcel_execute =await RepositoryParcel.execute_and_fetch(parcel_query)
        for item in parcel_execute :
            await RepositoryParcel.update_by_id(item.get('id'),{'status': 'کل سفارش کنسل شد '})



        return  ShowCancelInvoice(
            invoice_id=invoice_id,
            customer_name=execute_customer[0].get('name'),
            status=get_invoice[0].get('status'),

        )



@router.get('/set_share/')
async def set_share(vendor_id:int,num: int ):
    query_vendor= RepositoryVendor.select_where(RepositoryVendor.field('id').eq(vendor_id)).select('*')
    execute =await RepositoryVendor.execute_and_fetch(query_vendor)
    if not execute  :
        raise Exception('this vendor is not exist')
    percent = num / 100
    print(percent)
    name = {execute[0].get('name')}
    last_name = {execute[0].get('last_name')}
    if execute[0].get('share') != None:
            update_share=RepositoryVendor.update_by_id(vendor_id,{'share':execute[0].get('share')})
            return {'message': f'share {percent} with successfully updated for {name}{last_name} '}

    update_share = await RepositoryVendor.update_by_id(vendor_id, {'share': percent})
    return  {'message': f'share {percent} with successfully submit for {name} {last_name} '}

@router.get('/list_vendor/')
async def list_vendor():
    execute =await  RepositoryVendor.all()
    print(execute)
    vendor_list = []
    for item in execute :
        show=ShowVendorSchema(
            id = item.id,
            name = item.name,
            last_name = item.last_name ,
            phone = item.phone,
            balance=item.phone,

        )


        vendor_list.append(show)
    return  vendor_list


@router.get('/post_vendor/')
async def post_parcel_vendor(name:str,last_name:str):
    query_vendor = RepositoryVendor.select_where(RepositoryVendor.field('name').eq(name)).where(RepositoryVendor.field('last_name').eq(last_name)).select('*')
    execute =await RepositoryVendor.execute_and_fetch(query_vendor)
    costDelivery= []
    constFinally = 0
    # print(execute)
    if not execute :
        raise HTTPException(status_code=404,detail='vendor is not exist')
    query_parcel = RepositoryParcel.select_where(RepositoryParcel.field('vendor_id').eq(execute[0].get('id'))).select('*')
    execute_parcel = await RepositoryParcel.execute_and_fetch(query_parcel)

    if execute_parcel[0].get('status')== 'تایید شده توسط غرفه دار' :
        if not execute_parcel :
            raise HTTPException(status_code=404,detail='parcel is not exist')
        update =await RepositoryParcel.update_by_id(execute_parcel[0].get('id'),{'delivery':'مرسوله توسط غرفه دار ارسال شد ','pricedelivery':30000})

        query_invoice = RepositoryInvoice.select_where(RepositoryInvoice.field('id').eq(execute_parcel[0].get('invoice_id'))).select('*')
        execute_invoice = await RepositoryInvoice.execute_and_fetch(query_invoice)

        if not execute_invoice :
            raise HTTPException(status_code=404,detail='invoice is not exist')
        get_all_parcel = RepositoryParcel.select_where(RepositoryParcel.field('invoice_id').eq(execute_parcel[0].get('invoice_id'))).select('*')
        execute_parcel_all = await RepositoryParcel.execute_and_fetch(get_all_parcel)
        # print(execute_parcel_all)
        for index,value in enumerate(execute_parcel_all) :


            if value.get('pricedelivery') is not None :
                deliveryCost= value.get('pricedelivery')
                costDelivery.append(deliveryCost)
                for index,cost in enumerate(costDelivery):
                        constFinally +=cost
                print(value.get('status') == 'تایید شده توسط غرفه دار')
                print(value.get('delivery')=='مرسوله توسط غرفه دار ارسال شد ' )
                if value.get('delivery')=='مرسوله توسط غرفه دار ارسال شد ' and value.get('status') == 'تایید شده توسط غرفه دار' :
                    update_invoice =await RepositoryInvoice.update_by_id(execute_invoice[0].get('id'),{'status':'تایید شده توسط غرفه دار' ,'delivery':'ارسال شده توسط تمامی غرفه دار ها ','pricedelivery':constFinally})
                    query_customer = RepositoryCustomer.select_where(RepositoryCustomer.field('id').eq(execute_parcel[0].get('customer_id'))).select('*')
                    execute_customer = await RepositoryCustomer.execute_and_fetch(query_customer)
                    query_vendor = RepositoryVendor.select_where(RepositoryVendor.field('id').eq(value.get('vendor_id'))).select('*')
                    execute_vendor = await RepositoryVendor.execute_and_fetch(query_vendor)

                else :
                        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='سفارش شما هنوز به تایید غرفه دار نرسیده است ')
        print(execute_parcel[0])
        return ShowPostVendor(
                price_delivery=value.get('pricedelivery'),
                parcel_id=execute_parcel[0].get('id'),
                name_customer=execute_customer[0].get('name'),
                lastName_customer=execute_customer[0].get('last_name'),
                statusDelivery=value.get('status')
            )