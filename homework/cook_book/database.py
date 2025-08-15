from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL базы данных для асинхронного подключения SQLite
DATABASE_URL: str = "sqlite+aiosqlite:///./cook_book.db"

# Создание асинхронного движка SQLAlchemy
engine: AsyncEngine = create_async_engine(
    DATABASE_URL, echo=True  # включение логирования SQL-запросов для отладки
)

async_session: sessionmaker = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Базовый класс для декларативных моделей SQLAlchemy
Base: Any = declarative_base()
