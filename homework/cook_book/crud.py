from models import Recipe
from schemas import RecipeCreate
from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_recipe(session: AsyncSession, recipe: RecipeCreate) -> Recipe:
    """
    Создание нового рецепта в БД.

    :param session: AsyncSession - асинхронная сессия SQLAlchemy.
    :param recipe: RecipeCreate - данные рецепта для создания.
    :return: Recipe - созданный объект рецепта.
    """
    new_recipe: Recipe = Recipe(**recipe.model_dump())
    session.add(new_recipe)
    await session.commit()
    await session.refresh(new_recipe)
    return new_recipe


async def get_all_recipes(session: AsyncSession) -> list[Recipe]:
    """
    Получение списка всех рецептов, отсортированных по просмотрам и времени.

    :param session: AsyncSession - асинхронная сессия SQLAlchemy.
    :return: list[Recipe] - список всех рецептов.
    """
    stmt: Select[tuple[Recipe]] = select(Recipe).order_by(
        Recipe.views.desc(), Recipe.cooking_time.asc()
    )
    result: Result[tuple[Recipe]] = await session.execute(stmt)
    return list(result.scalars().all())


async def get_recipe_by_id(
    session: AsyncSession,
    recipe_id: int,
) -> Recipe | None:
    """
    Получение рецепта по его ID и увеличение счетчика просмотров.
    :param session: AsyncSession - асинхронная сессия SQLAlchemy.
    :param recipe_id: int - ID рецепта.
    :return: Recipe | None - объект рецепта или ничего, если рецепт не найден.
    """
    recipe: Recipe | None = await session.get(Recipe, recipe_id)
    if recipe:
        views: int = recipe.views
        recipe.views = views + 1
        await session.commit()
        await session.refresh(recipe)
    return recipe
