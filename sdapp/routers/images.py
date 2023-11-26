from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from sdapp.db import get_async_session
from sdapp.models import GeneratedImage
from sdapp.schemas.image_generation import (
    GeneratedImageCreate,
    GeneratedImageRead,
    GeneratedImageURL,
)
from sdapp.storage import Storage
from sdapp.workers.worker import text_to_image_task

router = APIRouter()


async def get_generated_image_or_404(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> GeneratedImage:
    select_query = select(GeneratedImage).where(GeneratedImage.id == id)
    result = await session.execute(select_query)
    image = result.scalar_one_or_none()

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return image


async def get_storage() -> Storage:
    return Storage()


@router.post(
    "/",
    response_model=GeneratedImageRead,
    status_code=status.HTTP_202_ACCEPTED,
)
async def generate_image(
    input: GeneratedImageCreate,
    session: AsyncSession = Depends(get_async_session),
) -> GeneratedImage:
    image = GeneratedImage(**input.model_dump())
    session.add(image)
    await session.commit()

    text_to_image_task.send(image.id)

    return image


@router.get("/{id}", response_model=GeneratedImageRead)
async def get_generated_image(
    image: GeneratedImage = Depends(get_generated_image_or_404),
) -> GeneratedImage:
    return image


@router.get("/{id}/url")
async def get_generated_image_url(
    request: Request,
    image: GeneratedImage = Depends(get_generated_image_or_404),
    storage: Storage = Depends(get_storage),
):
    if image.file_name is None:
        raise HTTPException(
            status=status.HTTP_400_BAD_REQUEST,
            detail="Image is not available yet. Please try again later.",
        )
    url = storage.get_url(request, image.file_name)
    return GeneratedImageURL(url=url)
