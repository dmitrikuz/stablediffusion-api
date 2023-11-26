from fastapi import APIRouter, Depends, HTTPException, Query
from sdapp.db import get_async_session
from sdapp.models import User
from sdapp.schemas.user import UserCreate, UserRead
from sdapp.utils import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/login")
async def get_user_page(page: int = Query(6, gt=5), size: int = 10):
    return {"page": page, "size": size}


@router.post(
    "/register",
    response_model=UserRead,
)
async def register_user(
    schema: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    hashed_password = get_password_hash(schema.password)

    registered_user = User(
        **schema.model_dump(
            exclude={
                "password",
            }
        ),
        hashed_password=hashed_password
    )
    session.add(registered_user)
    await session.commit()
    return registered_user
