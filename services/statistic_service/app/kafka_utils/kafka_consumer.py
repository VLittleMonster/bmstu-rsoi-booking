from aiokafka import AIOKafkaConsumer
from services import add_event_info
from database.database import Database
from schemas.dto import EventInfoDTO
import asyncio
import json

KAFKA_TOPIC = "booking.statistic.events.topic"
KAFKA_CONSUMER_GROUP = "group-id"
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"    # "kafka:29092"     # 'kafka_utils:9092'


async def consume(app_db: Database):
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        loop=asyncio.get_event_loop(),
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP
    )
    print("start consuming")
    await consumer.start()
    try:
        async for msg in consumer:
            event_info = EventInfoDTO.model_validate(json.loads(msg.value.decode('utf-8')))
            print(f"DTO event_info obj: {event_info}")
            db = app_db.get_session()
            await add_event_info(event_dto=event_info, db=db)
    except Exception as e:
        print(e)
    finally:
        await consumer.stop()
