import asyncio
import uuid

from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.middleware import Middleware
from sqlalchemy.sql import select

import dramatiq
from sdapp.db import async_session_maker
from sdapp.logger import logger
from sdapp.models import GeneratedImage
from sdapp.schemas.image_generation import (
    GeneratedImageCreate,
    GeneratedImageRead,
    GeneratedImageURL,
)
from sdapp.settings import settings
from sdapp.storage import Storage
from sdapp.transformers.text_to_image import TextToImage


class TextToImageMiddleware(Middleware):
    def __init__(self) -> None:
        super().__init__()
        self.text_to_image = TextToImage()

    def after_process_boot(self, broker):
        self.text_to_image.load_model()
        return super().after_process_boot(broker)


text_to_image_middleware = TextToImageMiddleware()
redis_broker = RedisBroker(host=settings.redis_host)
redis_broker.add_middleware(text_to_image_middleware)
dramatiq.set_broker(redis_broker)


def get_image(id: int) -> GeneratedImage:
    async def _get_image(id: int) -> GeneratedImage:
        async with async_session_maker() as session:
            select_query = select(GeneratedImage).where(GeneratedImage.id == id)
            result = await session.execute(select_query)
            image = result.scalar_one_or_none()

            if image is None:
                raise Exception("Image does not exist", id)

            return image

    return asyncio.get_event_loop().run_until_complete(_get_image(id))


def update_progress(image: GeneratedImage, step: int):
    async def _update_progress(image: GeneratedImage, step: int):
        async with async_session_maker() as session:
            async with session.begin():
                image.progress = int((step / image.num_steps) * 100)
                session.add(image)
            await session.commit()

    asyncio.get_event_loop().run_until_complete(_update_progress(image, step))


def update_file_name(image: GeneratedImage, file_name: str):
    async def _update_progress(image: GeneratedImage, file_name: str):
        async with async_session_maker() as session:
            async with session.begin():
                image.file_name = file_name
                session.add(image)
            await session.commit()

    asyncio.get_event_loop().run_until_complete(_update_progress(image, file_name))


@dramatiq.actor()
def text_to_image_task(image_id: int):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    image = get_image(image_id)

    def callback(pipe, step, timestep, callback_kwargs):
        update_progress(image, step)
        return callback_kwargs

    image_output = text_to_image_middleware.text_to_image.generate(
        image.prompt, callback=callback
    )

    file_name = f"{uuid.uuid4()}.png"

    storage = Storage()
    storage.upload_image(image_output, file_name)

    update_file_name(image, file_name)

    loop.close()
