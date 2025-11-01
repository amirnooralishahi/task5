import asyncio
import json
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

class kafka:
    def __init__(self, data):
        self.data = data

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
        )
        await self.producer.start()

    async def get_data(self):
        parcel_id = self.data[0].get('id')
        time_create = self.data[0].get('created_at')
        parcel = {parcel_id: str(time_create)}  # datetime → string
        print("📦 Data prepared:", parcel)
        return parcel

    async def produce(self):
        parcel = await self.get_data()
        await self.producer.send_and_wait('check_parcel_time', value=parcel)
        print("✅ Message sent to Kafka topic 'check_parcel_time':", parcel)

    async def stop(self):
        await self.producer.stop()

    async def consumer(self):
        consumer = AIOKafkaConsumer(
            'check_parcel_time',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        )
        await consumer.start()
        try:
            async for msg in consumer:
                print(
                    f"Received message: {msg.value}"
                )
        finally:
            await consumer.stop()
