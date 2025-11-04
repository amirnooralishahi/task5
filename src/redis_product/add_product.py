import datetime
import json
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from confluent_kafka.admin import AdminClient
from redis.asyncio import Redis


class Kafka:


    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda m: json.dumps(m).encode('utf-8'),

        )

        await self.producer.start()

    async def stop(self):
            await self.producer.stop()

    async def produce(self,customer_id,vendor_id,value):
            topic_name = f'add-parcel-{customer_id}-{vendor_id}'
            await self.producer.send(topic=topic_name, value=value)

