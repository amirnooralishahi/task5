from typing import List

from hepler.helper_parcel import get_and_check_entity
from repository.parcelRepo import RepositoryParcel
from kafkaProject.expirationParcel import kafka

class checkParcelExpire :

    def __init__(self,parcel_id:List[int]|int,time:int)->None:
        self.parcel_id=parcel_id
        self.time=time



    async def process(self)->dict:
        if isinstance(self.parcel_id, str):
            parcel_ids = [int(p.strip()) for p in self.parcel_id.split(',') if p.strip().isdigit()]
        elif isinstance(self.parcel_id, list):
            parcel_ids = []
            for p in self.parcel_id:
                if isinstance(p, str) and ',' in p:
                    parcel_ids.extend([int(x.strip()) for x in p.split(',') if x.strip().isdigit()])

                elif str(p).isdigit():
                    parcel_ids.append(int(p))
        else:
            parcel_ids = []

        execute = await get_and_check_entity(
            RepositoryParcel,
            identifier=parcel_ids,
            field_name='id',
        )
        kafka_manager = kafka()
        await kafka_manager.consumer(self.time, execute)
        return {'message': 'with successfully set time'}