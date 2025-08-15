from database import Base
from sqlalchemy import Column, Integer, String, Text


class Recipe(Base):
    """Модель SQLAlchemy для таблицы рецептов."""

    __tablename__ = "recipes"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    title: Column[str] = Column(String, index=True, nullable=False)
    views: Column[int] = Column(Integer, default=0)
    cooking_time: Column[int] = Column(Integer, nullable=False)
    ingredients: Column[str] = Column(Text, nullable=False)
    description: Column[str] = Column(Text, nullable=False)
