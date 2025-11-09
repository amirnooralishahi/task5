from typing import  Any,  List, Union
from fastapi import APIRouter, Query
from service.list_vendor import ListVendorService
from src.Controller.submit_parcel_by_vendor_controller import submitParcelByVendorController
from src.Controller.add_product_by_vendor_controller import AddProductByVendor
from src.Controller.cancel_one_parcel_controller import cancelOneParcelController
from src.Controller.check_parcel_expire import checkParcelExpire
from src.Controller.post_parcel_vendor_controller import PostParcelVendorController
from src.Controller.set_share_controller import SetShare
from src.schema.SchemaSendPostVendor import ShowPostVendor
from InputResponseSchema.get_show_item_to_vendor_schema import ShowCancelParcel, ShowCancelInvoice
from src.Controller.send_product_to_customer_controller import SendProductToCustomerController
from src.Controller.get_show_item_to_vendor_controller import getShowItemToVendorController
from src.Controller.all_list_product_controller import AllListProductController
from src.Controller.get_show_item_to_customer import getShowItemToCustomer
from src.Controller.cancel_invoice import  cancelInvoice
router = APIRouter(
    prefix='/parcel',
    tags=['parcel']
)

"جرنی کامل خرید"
"ارسال سفارش توسط هر فروشنده"
"نمایش جزییات خرید به مشتری"
"نمایش جزییاس سفارش برای هر فروشنده"
"امکان تنظیم کارمزد برای هر فروشنده توسط ادمین"


#از این استفاده نکردم
@router.get('send_product_to_customer/{parcel_id}')
async def send_product_to_customer(parcel_id:int ):
       return  await SendProductToCustomerController.process(parcel_id)

@router.get('/vendor/list_product/')
async def all_list_product():
    response = AllListProductController()
    return  await response.process()
@router.get('/parcel-customer/')
async def get_parcel_for_customer(name:str , last_name:str):
    return await getShowItemToCustomer(name=name , last_name= last_name).process()


@router.get('/parcel/',response_model=ShowCancelParcel)
async def cancel_one_parcel(parcel_id: int,name:str , last_name:str):
        return await cancelOneParcelController(parcel_id=parcel_id, name=name, last_name=last_name).process()
@router.get('/parcel-vendor/')
async def get_parcelItem_for_vendor(name:str , last_name:str):
        return await getShowItemToVendorController(name=name,last_name=last_name).process()

# @router.post('/add_parcel/')
# async def add_item_parcel(name: str, last_name: str, data: Dict[str, Dict[str, Any]] = CreateParcelSchema):
#         return  await addItemParcel(name=name, last_name=last_name, data=data).process()

@router.get('/cancel_invoice/',response_model=ShowCancelInvoice)
async def cancel_invoice(invoice_id:int,name:str ,last_name:str):
        return await  cancelInvoice(name=name,last_name=last_name,invoice=invoice_id).process()


@router.get('/submit/')
async def submit_parcel(parcel_id: Union[List[int],int] = Query(alias="parcel_id", description='list of parcel id for confirm')) :
    return await submitParcelByVendorController(parcel_id=parcel_id).process()




@router.get('/set_share/')
async def set_share(vendor_id:int,num: int ):
        return await SetShare(vendor_id=vendor_id, num=num).process()

@router.get('/list_vendor/')
async def list_vendor():
        ser =await ListVendorService().process()
        return ser


@router.get('/post_vendor/',response_model=ShowPostVendor)
async def post_parcel_vendor(name:str,last_name:str):
    return await PostParcelVendorController(name=name,last_name=last_name).process()


@router.get('/check_parcel_expire/')
async def check_parcel_expire(time,parcel_id=Union[List[int],int]):
        return await checkParcelExpire(time=time , parcel_id=parcel_id).process()

@router.post('/add-product-by-vendor/')
async def add_product_by_vendor(name:str,last_name:str, data:dict[str,Any]):

           return  await AddProductByVendor(name=name,last_name=last_name,data=data).process()