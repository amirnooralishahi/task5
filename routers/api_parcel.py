import datetime
import decimal
from typing import Dict, Any, Set, Tuple,List
from fastapi import APIRouter,HTTPException,status

from Enum.EnumInvoice import EnumInvoice
from repository.Customer import RepositoryCustomer
from repository.Invoice import RepositoryInvoice
from repository.Vendor import RepositoryVendor
from repository.parcelRepo import RepositoryParcel
from repository.parcelItem import RepositoryItem
from repository.product import RepositoryProduct
from schema.SchemShowProduct import ShowProductSchema
from schema.SchemaInvoice import CreateInvoiceSchema
from schema.SchemaParcel import CreateParcelSchema
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
    query_customer =await RepositoryCustomer.get_customer(name=name , last_name=last_name)
    query = RepositoryInvoice.select_where(RepositoryInvoice.field('customer_id') == query_customer.id).select('id')
    execute =await RepositoryInvoice.execute_and_fetch(query)
    invoice_id = execute[0].get('id')
    query_parcel= RepositoryParcel.select_where(RepositoryParcel.field('invoice_id').eq(invoice_id)).select('*')
    execute_parcel =await RepositoryParcel.execute_and_fetch(query_parcel)

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

    return show_list


@router.get('/parcel/',response_model=ShowCancelParcel)
async def cancel_one_parcel(parcel_id: int,name:str , last_name:str):
    query_customer=await RepositoryCustomer.get_customer(name,last_name)
    if query_customer:
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

        for i in execute_item:
            query_product = RepositoryProduct.select_where(
                RepositoryProduct.field('id').eq(i.get('product_id'))).select('*')
            execute_product = await RepositoryProduct.execute_and_fetch(query_product)
            name_product = execute_product[0].get('name')
            price_product = execute_product[0].get('price')
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
async def add_item_parcel(name:str,last_name:str,data:dict[str,dict[str,Any]]=CreateParcelSchema):
    get_customer =await RepositoryCustomer.get_customer(name=name,last_name=last_name)

    get_invoice = await RepositoryInvoice.get_invoice(get_customer.id)
    value_invoice ={
        "customer_id":get_customer.id,
        'status':EnumInvoice.INVOICE_AWAIT_FOR_CONFIRM,
    }
    if not get_invoice:
        invoice = await RepositoryInvoice.create_return(value_invoice)
        invoice_id = invoice
        print(invoice_id)

    else:
        invoice = await RepositoryInvoice.get_invoice(get_customer.id)
        for keyInvoice, valueInvoice in enumerate(invoice):
            invoice_id = valueInvoice.id
        print(invoice_id)

    unique_vendor_keys: Set[Tuple[str, str]] = set()
    structured_data = {}

    for key, value in data.get('data').items():
        vendor_name, vendor_last_name = key.split('-', 1)
        unique_vendor_keys.add((vendor_name, vendor_last_name))
        structured_data[key] = value

    vendor_names = [v[0] for v in unique_vendor_keys]
    vendor_last_names = [v[1] for v in unique_vendor_keys]
    query_vendors = await RepositoryVendor.get_vendor(name=vendor_names,last_name=vendor_last_names)



    if not query_vendors :
        raise HTTPException(status_code=404, detail='this vendor does not exist')

    vendor_map = {
        f"{values.name}-{values.last_name}":values.id

        for keys, values in enumerate(query_vendors)
    }
    totalPrice = []
    countProduct = []
    vendor_id_list = []
    share_company_parcel=[]
    nameProduct = []
    current_parcelItem_data={}
    for key in structured_data.keys():
        vendor_id_list.append(vendor_map[key])
    vendor =await RepositoryVendor.find_by_many_id(vendor_id_list)
    resultVendor = {
        v.id: v for v in vendor
    }

    for vendor_key, products_list in structured_data.items():
        vendor_id = vendor_map.get(vendor_key)
        get_vendor = resultVendor.get(vendor_id)

        if not get_vendor:
            raise HTTPException(status_code=404, detail='this vendor does not exist')
        vendor_share = get_vendor.share

        for item in products_list:
            nameProduct.append(item['product_name'])
            totalPrice.append(int(item['price'])*int(item['count']))
            countProduct.append(item['count'])
            share_company_parcel.append((int(item['price'])*int(item['count']))*vendor_share)

    product =await RepositoryProduct.get_product_many(nameProduct)


    count=0
    parcel={}

    for num in range(0,len(vendor_id_list)):

        production = {
                    #update,create,priceDelivery
                  'vendor_id': vendor_id_list[num],
                  'customer_id': get_customer.id,
                  'price': sum(totalPrice),
                  'count': sum(countProduct),
                  'share_company': decimal.Decimal(sum(share_company_parcel)),
                  'invoice_id': invoice_id,
                  'created_at': datetime.datetime.now(),
                  'origin': get_customer.city,
                  'status': EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM,
                  'delivery':EnumInvoice.STATUS_DELIVERY,
                  'methodpost':EnumInvoice.METHOD_POST
                   }

        unique_record_key = str(count)
        count += 1

        if  vendor_id_list[num] not in parcel:
            parcel[vendor_id_list[num]] = {}
        id = vendor_id_list[num]
        parcel[id][unique_record_key] = production

    records_to_insert = [
        record
        for vendor_records in parcel.values()

        for record in vendor_records.values()
    ]

    get_parcel = await RepositoryParcel.get_parcel(customer_id=get_customer.id ,vendor_id= vendor_id_list)
    vendor_parcel_list= {}
    parcel_id_list = []
    if not get_parcel:
        parcel_id =await RepositoryParcel.create_return_many(records_to_insert)
        for id in parcel_id:
            parcel_id_list.append(id.id)
            vendor_parcel_list[id.vendor_id]=id.sid
    else:
        for id in range(0,len(get_parcel)):

            parcel_id = get_parcel[id].id
            parcel_id_list.append(parcel_id)
            vendor_parcel_list[get_parcel[id].vendor_id]=get_parcel[id].id

    for parcelItem in range(0,len(nameProduct)) :
        if product[parcelItem].vendor_id   in vendor_parcel_list:
           current_parcelItem_data[parcelItem] =  {
            'parcel_id': vendor_parcel_list[product[parcelItem].vendor_id],
            'product_id': product[parcelItem].id,
            'price': product[parcelItem].price,
            'count': countProduct[parcelItem],
            'share_company': int(share_company_parcel[parcelItem]),
        }

    amir = [ recordParcelItem for recordParcelItem in current_parcelItem_data.values() ]
    createProduct =await RepositoryItem.create_return_many(amir)
    return {'message':'with successfully conferim'}




@router.get('/cancel_invoice/',response_model=ShowCancelInvoice)
async def cancel_invoice(invoice_id:int,name:str ,last_name:str):
    execute_customer=await RepositoryCustomer.get_customer(name,last_name)
    query =await RepositoryInvoice.find_by_id(invoice_id)
    parcel_query = RepositoryParcel.get_parcel(invoice_id)
    if not execute_customer :
        raise HTTPException(status_code=404,detail='customer is not exist')
    if query:
        await RepositoryInvoice.update_by_id(query.id, {'status': 'کل سفارش کنسل شد '})
        for item in parcel_query :
            await RepositoryParcel.update_by_id(item.get('id'),{'status': 'کل سفارش کنسل شد '})
        return  ShowCancelInvoice(
            invoice_id=invoice_id,
            customer_name=execute_customer[0].get('name'),
            status=query.status,
        )


from fastapi import Query

@router.get('/submit/')
async def add_confirm(parcel_id: List[int] = Query(alias="parcel_id",description='list of parcel id for confirm')) :
        for item in parcel_id:
            query_parcel = RepositoryParcel.get_parcel(item)
            if not query_parcel :
                raise HTTPException(status_code=404,detail='parcel is not exist')

            if query_parcel.status =='تایید شده توسط غرفه دار' :
                raise HTTPException(status_code=422,detail='this parcel already submitted')

            change_status=await RepositoryParcel.update_by_id(query_parcel.id,{'status':'تایید شده توسط غرفه دار'})





@router.get('/set_share/')
async def set_share(vendor_id:int,num: int ):
    query_vendor=await RepositoryVendor.find_by_id(vendor_id)

    if not query_vendor:
        raise Exception('this vendor is not exist')
    percent = num / 100
    name = {query_vendor.name}
    last_name = {query_vendor.last_name}
    if query_vendor.share!= None:
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
    if not execute :
        raise HTTPException(status_code=404,detail='vendor is not exist')
    query_parcel = RepositoryParcel.select_where(RepositoryParcel.field('vendor_id').eq(execute[0].get('id'))).select('*')
    execute_parcel = await RepositoryParcel.execute_and_fetch(query_parcel)

    if execute_parcel[0].get('status')== 'تایید شده توسط غرفه دار' :
        if not execute_parcel :
            raise HTTPException(status_code=404,detail='parcel is not exist')
        update =await RepositoryParcel.update_by_id(execute_parcel[0].get('id'),{'delivery':'مرسوله توسط غرفه دار ارسال شد ','pricedelivery':30000})

        query_invoice =await RepositoryInvoice.find_by_id(execute_parcel[0].get('invoice_id'))

        if not query_invoice:
            raise HTTPException(status_code=404,detail='invoice is not exist')
        get_all_parcel = RepositoryParcel.select_where(RepositoryParcel.field('invoice_id').eq(execute_parcel[0].get('invoice_id'))).select('*')
        execute_parcel_all = await RepositoryParcel.execute_and_fetch(get_all_parcel)
        for index,value in enumerate(execute_parcel_all) :


            if value.get('pricedelivery') is not None :
                deliveryCost= value.get('pricedelivery')
                costDelivery.append(deliveryCost)
                for index,cost in enumerate(costDelivery):
                        constFinally +=cost

                if value.get('delivery')=='مرسوله توسط غرفه دار ارسال شد ' and value.get('status') == 'تایید شده توسط غرفه دار' :
                    update_invoice =await RepositoryInvoice.update_by_id(query_invoice.id,{'status':'تایید شده توسط غرفه دار' ,'delivery':'ارسال شده توسط تمامی غرفه دار ها ','pricedelivery':constFinally})
                    query_customer =await RepositoryCustomer.find_by_id(execute_parcel[0].get('id'))
                    query_vendor = RepositoryVendor.select_where(RepositoryVendor.field('id').eq(value.get('vendor_id'))).select('*')
                    execute_vendor = await RepositoryVendor.execute_and_fetch(query_vendor)

                else :
                        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='سفارش شما هنوز به تایید غرفه دار نرسیده است ')

        return ShowPostVendor(
                price_delivery=value.get('pricedelivery'),
                parcel_id=execute_parcel[0].get('id'),
                name_customer=query_customer.name,
                lastName_customer=query_customer.last_name,
                statusDelivery=value.get('status')
            )



