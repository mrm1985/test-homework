from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# URL базы данных для асинхронного подключения SQLite
DATABASE_URL: str = "sqlite+aiosqlite:///./cook_book.db"

# Создание асинхронного движка SQLAlchemy
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
