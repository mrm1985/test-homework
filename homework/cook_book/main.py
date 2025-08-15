from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from crud import create_recipe, get_all_recipes, get_recipe_by_id
from database import async_session, engine
from fastapi import Depends, FastAPI, HTTPException
from models import Base
from schemas import RecipeCreate, RecipeDetail, RecipeRead
from sqlalchemy.ext.asyncio import AsyncSession


# Функция зависимости для получения сессии
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Обработчик жизненного цикла приложения."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app: FastAPI = FastAPI(
    lifespan=lifespan,
    title="API кулинарной книги",
    description="API для управления рецептами в кулинарной книге",
)


@app.post(
    "/recipes",
    response_model=RecipeRead,
    summary="Создание нового рецепта",
)
async def create(
        recipe: RecipeCreate,
        session: AsyncSession = Depends(get_session),
) -> RecipeRead:
    """Создание нового рецепта в БД."""
    return await create_recipe(session, recipe)


@app.get(
    "/recipes",
    response_model=list[RecipeRead],
    summary="Получение списка рецептов",
)
async def read_all(
        session: AsyncSession = Depends(get_session),
) -> list[RecipeRead]:
    """Получение списка всех рецептов, отсортированных по просмотрам и времени приготовления."""
    return await get_all_recipes(session)


@app.get(
    "/recipes/{recipe_id}",
    response_model=RecipeDetail,
    summary="Получение деталей рецепта",
)
async def read_one(
        recipe_id: int,
        session: AsyncSession = Depends(get_session),
) -> RecipeDetail:
    """Получение детальной информации о рецепте по его ID."""
    recipe: Any | None = await get_recipe_by_id(session, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    return recipe


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
