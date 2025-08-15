from pydantic import BaseModel, ConfigDict, Field


class RecipeCreate(BaseModel):
    """Модель для создания рецепта."""

    title: str = Field(
        ...,
        description="Название рецепта.",
        min_length=1,
        max_length=255,
    )
    cooking_time: int = Field(
        ...,
        description="Время приготовления в минутах.",
        gt=0,
    )
    ingredients: str = Field(
        ...,
        description="Список ингредиентов.",
        min_length=1,
    )
    description: str = Field(
        ...,
        description="Описание рецепта.",
        min_length=1,
    )


class RecipeRead(BaseModel):
    """Модель для чтения полной информации о рецепте."""

    id: int = Field(
        ...,
        description="ID рецепта.",
    )
    title: str = Field(
        ...,
        description="Название рецепта.",
    )
    views: int = Field(
        ...,
        description="Количество просмотров рецепта.",
    )
    cooking_time: int = Field(
        ...,
        description="Время приготовления рецепта в минутах.",
    )

    model_config = ConfigDict(from_attributes=True)


class RecipeDetail(RecipeRead):
    """Модель для чтения детальной информации о рецепте."""

    ingredients: str = Field(
        ...,
        description="Список ингредиентов.",
    )
    description: str = Field(
        ...,
        description="Детальное описание рецепта.",
    )
