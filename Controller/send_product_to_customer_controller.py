from hepler.helper_parcel import get_and_check_entity
from repository.Invoice import RepositoryInvoice
from repository.parcelRepo import RepositoryParcel


from fastapi import FastAPI,APIRouter
router = APIRouter()

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
