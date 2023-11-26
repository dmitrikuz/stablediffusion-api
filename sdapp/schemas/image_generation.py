from datetime import datetime

from pydantic import BaseModel


class GeneratedImageBase(BaseModel):
    prompt: str

    class Config:
        from_attributes = True


class GeneratedImageCreate(GeneratedImageBase):
    pass


class GeneratedImageRead(GeneratedImageBase):
    id: int
    created_at: datetime
    progress: int
    file_name: str | None


class GeneratedImageURL(BaseModel):
    url: str
