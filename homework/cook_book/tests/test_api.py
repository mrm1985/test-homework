import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..main import app, get_session
from ..models import Base


@pytest.fixture
async def test_session():
    """Фикстура для создания тестовой базы данных в памяти."""
    test_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )
    async_session = sessionmaker(
        bind=test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture
async def client(test_session):
    """Фикстура для создания асинхронного тестового клиента."""
    app.dependency_overrides[get_session] = lambda: test_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_create_recipe(client):
    """Тестирует создание рецепта."""
    recipe_data = {
        "title": "Тестовый рецепт",
        "cooking_time": 30,
        "ingredients": "Мука, вода, соль",
        "description": "Простое тесто для выпечки.",
    }
    response = await client.post("/recipes", json=recipe_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == recipe_data["title"]
    assert data["cooking_time"] == recipe_data["cooking_time"]
    assert data["views"] == 0
    assert data["id"] == 1


@pytest.mark.asyncio
async def test_get_all_recipes(client):
    """Тестирует получение списка всех рецептов."""
    recipe_data = {
        "title": "Тестовый рецепт",
        "cooking_time": 30,
        "ingredients": "Мука, вода, соль",
        "description": "Простое тесто для выпечки.",
    }
    await client.post("/recipes", json=recipe_data)
    response = await client.get("/recipes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == recipe_data["title"]


@pytest.mark.asyncio
async def test_get_recipe_by_id(client):
    """Тестирует получение рецепта по ID и увеличение счетчика просмотров."""
    recipe_data = {
        "title": "Тестовый рецепт",
        "cooking_time": 30,
        "ingredients": "Мука, вода, соль",
        "description": "Простое тесто для выпечки.",
    }
    response = await client.post("/recipes", json=recipe_data)
    recipe_id = response.json()["id"]

    response = await client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == recipe_data["title"]
    assert data["ingredients"] == recipe_data["ingredients"]
    assert data["description"] == recipe_data["description"]
    assert data["views"] == 1

    # Проверяем увеличение счетчика просмотров
    response = await client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    assert response.json()["views"] == 2


@pytest.mark.asyncio
async def test_get_recipe_not_found(client):
    """Тестирует обработку несуществующего рецепта."""
    response = await client.get("/recipes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Рецепт не найден"
