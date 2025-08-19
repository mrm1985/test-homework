from typing import Any

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base: Any = declarative_base()


class Recipe(Base):
    """Модель SQLAlchemy для таблицы рецептов."""

    __tablename__ = "recipes"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0)
    cooking_time: Mapped[int] = mapped_column(Integer, nullable=False)
    ingredients: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
