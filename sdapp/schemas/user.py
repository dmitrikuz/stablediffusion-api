from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=7)


class User(UserBase):
    id: int
    hashed_password: str


class UserRead(UserBase):
    id: int
