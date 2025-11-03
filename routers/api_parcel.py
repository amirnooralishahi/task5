import datetime
import decimal
from traceback import print_tb
from typing import Dict, Any, Set, Tuple, List, Union
from fastapi import APIRouter,HTTPException,status,Query
from decimal import Decimal
import kafkaProject.expirationParcel
from Controller.cancel_one_parcel_controller import cancelOneParcelController
from Controller.check_parcel_expire import checkParcelExpire
from Controller.list_vendor import listVendor
from Controller.post_parcel_vendor_controller import PostParcelVendorController
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
from Controller.send_product_to_customer_controller import sendProductToCustomerController
from Controller.get_show_item_to_parcel import getShowItemToVendorController
from Controller.allListProductController import AllListProductController
from Controller.get_show_item_to_customer import getShowItemToCustomer
from Controller.cancel_invoice import  cancelInvoice
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
       return  await sendProductToCustomerController.process(parcel_id)

@router.get('/vendor/list_product/')
async def all_list_product():
    return  AllListProductController()
@router.get('/parcel-customer/')
async def get_parcel_for_customer(name:str , last_name:str):
    return  getShowItemToCustomer(name=name , last_name= last_name)


@router.get('/parcel/',response_model=ShowCancelParcel)
async def cancel_one_parcel(parcel_id: int,name:str , last_name:str):
        return cancelOneParcelController(parcel_id=parcel_id, name=name, last_name=last_name)
@router.get('/parcel-vendor/')
async def get_parcelItem_for_vendor(name:str , last_name:str):
        return getShowItemToVendorController(name=name,last_name=last_name)

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
        name_vendor = vendor.split('-')[0]
        last_name_vendor = vendor.split('-')[1]
        for item in choice_product:
            print(item)
            list_product.append({
                'vendor_name':name_vendor,
                'vendor_last_name':last_name_vendor,
                'nameProduct':item.get('product_name'),
                'price':item.get('price'),
                'count':item.get('count'),
            })


    total_amount = 0
    total_item_count = 0
    total_share_company = decimal.Decimal(0)
    productive: List[Dict[str, Any]] = []
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

    sum_total_price=[]
    sum_count_product=[]
    sum_share_company=[]
    dictProduct ={'name': name_product,
                  'price': item_price,
                  'count': item_count }
    update=await check_and_buy_item(vendor_id_list,dictProduct,customer_id)
    if update !=status.HTTP_200_OK:
        raise HTTPException(status_code=406, detail='موجودی کافی نیست')
    current_vendor_items: List[Dict[str, Any]] = []
    create_parcelItem=[]
    production={}
    for item in list_product:

        vendor_id = next(
            (v.get('id') for v in vendor_info if
             v.get('name') == item['vendor_name'] and v.get('last_name') == item['vendor_last_name']),
            None
        )

        if vendor_id is None:
            raise HTTPException(status_code=400, detail=f"غرفه دار {item['vendor_name']} یافت نشد.")

        vendor_share_rate = vendor_share_map.get(vendor_id, 0)  # نرخ سهم غرفه دار

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
        total_amount += total_item_price
        sum_total_price.append(total_amount)
        total_item_count += item_count
        sum_count_product.append(total_item_count)
        total_share_company += share_company_cost
        sum_share_company.append(total_share_company)
        current_vendor_items.append(parcel_item_data)
        key_vendor = 'vendor_id'

        if key_vendor not in production :
            production[key_vendor] =vendor_id
        elif production[key_vendor] == vendor_id :
             production[key_vendor] = None
        if item == list_product[-1]:
            productionUpdate = {

                'customer_id': customer_id,
                'price': sum(sum_total_price),
                'count': sum(sum_count_product),
                'share_company': sum(sum_share_company),
                'invoice_id': get_invoice[0].id,
                'created_at': datetime.datetime.now(),
                'origin': customer_origin,
                'status': EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM,
                'delivery': EnumInvoice.STATUS_DELIVERY,
                'methodpost': EnumInvoice.METHOD_POST
            }
            production.update(productionUpdate)
            productive.append(production)
            print(productive)
            get_parcel = await RepositoryParcel.get_parcel(vendor_id=[vendor_id], customer_id=customer_id)

            sum_total_price=[]
            sum_count_product=[]
            sum_share_company=[]






    print(productive)

    # if not get_parcel:
    #     create_parcels = await RepositoryParcel.create_return_many(productive)
    #     new_parcel_id = create_parcels[0].id
    #     for item_data in current_vendor_items:
    #         item_data['parcel_id'] = new_parcel_id
    #         current_parcelItem_data.append(item_data)

        # get_parcel = create_parcels
    # else:
    #     existing_parcel_id = get_parcel[0].id
    #
    #     for item_data in current_vendor_items:
    #         item_data['parcel_id'] = existing_parcel_id
    #     await RepositoryItem.create_return_many(current_vendor_items)
    # kafka_manager = kafka()
    # await kafka_manager.start()
    # await kafka_manager.produce(get_parcel)
    # await kafka_manager.stop()
    # createProduct = await RepositoryItem.create_return_many(current_parcelItem_data)
    #
    #
    #
    # return ProductParcelSchema(
    #     vendor_id=vendor_id_list,
    #     customer_id= customer_id,
    #     price=total_amount,
    #     count=total_item_count,
    #     share_company=int(total_share_company),
    #     invoice_id=get_invoice[0].id,
    #     created_at=datetime.datetime.now(),
    #     origin= customer_origin,
    #     status=EnumInvoice.PARCEL_AWAIT_FOR_CONFIRM,
    #     delivery=EnumInvoice.STATUS_DELIVERY,
    #     methodpost=EnumInvoice.METHOD_POST
    # )

@router.get('/cancel_invoice/',response_model=ShowCancelInvoice)
async def cancel_invoice(invoice_id:int,name:str ,last_name:str):
        return  cancelInvoice(name=name,last_name=last_name,invoice=invoice_id)


@router.get('/submit/')
async def add_confirm(parcel_id: Union[List[str],str] = Query(alias="parcel_id",description='list of parcel id for confirm')) :
    return add_confirm(parcel_id=parcel_id)




@router.get('/set_share/')
async def set_share(vendor_id:int,num: int ):
        return await set_share(vendor_id=vendor_id, num=num)

@router.get('/list_vendor/')
async def list_vendor():
        return   listVendor


@router.get('/post_vendor/',response_model=ShowPostVendor)
async def post_parcel_vendor(name:str,last_name:str):
    return PostParcelVendorController(name=name,last_name=last_name)


@router.get('/check_parcel_expire/')
async def check_parcel_expire(time,parcel_id=Union[List[int],int]):
        return  checkParcelExpire(time=time,parcel_id=parcel_id)

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
