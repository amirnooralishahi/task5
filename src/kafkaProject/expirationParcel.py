import asyncio
import datetime
import json
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from src.Enum.EnumInvoice import EnumInvoice
from hepler.helper_parcel import get_and_check_entity, get_and_update
from src.repository.parcelRepo import RepositoryParcel


class kafka:


    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
        )
        await self.producer.start()



    async def produce(self,data):

        if isinstance(data[0], object):
            parcel_id = data[0].id
            time_create = data[0].created_at
            parcel = {parcel_id: str(time_create)}  # datetime → string
            await self.producer.send_and_wait('check_parcel_time', value=parcel)
        elif isinstance(data[0], dict):
            parcel_id = data[0].get('id')
            time_create = data[0].get('created_at')
            parcel = {parcel_id: str(time_create)}
            await self.producer.send_and_wait('check_parcel_time', value=parcel)
        print("✅ Message sent to Kafka topic 'check_parcel_time':", parcel)

    async def stop(self):
        await self.producer.stop()

    async def consumer(self,time:int,execute):
        consumer = AIOKafkaConsumer(
            'check_parcel_time',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        )
        saveID = []
        currentTime= datetime.datetime.now()
        dateTime = int(time)
        await consumer.start()
        try:
            print(dateTime)
            timeAgo = datetime.timedelta(hours=(dateTime))

            async for msg in consumer:
                for item in msg.value:
                    if execute[0].get('id') == int(item)  :
                        print(
                            f"Received message: {msg.value[item]}"
                        )
                    if currentTime> datetime.datetime.fromisoformat(msg.value[item])-timeAgo:
                        saveID.append(int(item))

                await get_and_update(
                    RepositoryParcel,
                    identifier=saveID,
                    field_name='id',
                    dict_update={'status':EnumInvoice.CANCEL_BY_SYSTEM_TIMEOUT}
                )
                return {'message':'with successfully canceled'}

        finally:

            await consumer.stop()
