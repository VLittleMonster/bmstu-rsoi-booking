from aiokafka import AIOKafkaProducer
import asyncio
import json
import uuid
from random import randint
from schemas.dto import EventInfoMsg


class KafkaProducer:
    KAFKA_TOPIC = "booking.statistic.events.topic"
    KAFKA_BOOTSTRAP_SERVERS = "kafka:29092"
    __background_tasks = set()

    @staticmethod
    async def __send(msg: EventInfoMsg):
        producer = AIOKafkaProducer(
            loop=asyncio.get_event_loop(),
            bootstrap_servers=KafkaProducer.KAFKA_BOOTSTRAP_SERVERS
        )
        await producer.start()
        try:
            value_json = EventInfoMsg.model_dump_json(msg).encode("utf-8")
            print(f'Sending msg json: {value_json}')
            await producer.send_and_wait(KafkaProducer.KAFKA_TOPIC, value_json)
        except Exception as e:
            print(f"KafkaSendingError: {e}")
        finally:
            await producer.stop()

    @staticmethod
    def send(msg: EventInfoMsg):
        msg.eventUuid = str(uuid.uuid4())
        print(f'Sending event_info obj: {msg}')
        task = asyncio.create_task(KafkaProducer.__send(msg))
        KafkaProducer.__background_tasks.add(task)
        task.add_done_callback(KafkaProducer.__background_tasks.discard)
