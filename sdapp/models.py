from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(1024), index=True, unique=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False)


class GeneratedImage(Base):
    __tablename__ = "generated_images"

    id: Mapped[datetime] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    num_steps: Mapped[int] = mapped_column(Integer, nullable=False, default=50)

    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)