from typing import Optional, List

from sqlalchemy import UniqueConstraint, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlmodel import Field, SQLModel, Relationship

from app.utils.db import Base
from recipes.tests.test_data import example_ingredient



class Ingredient(Base):
    """
    Nutritional values by default refer to 100g serving.
    """
    __tablename__ = "ingredient"
    __table_args__ = (UniqueConstraint("name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    # NutritionalValues
    calories: Mapped[float] = mapped_column(default=0.0)
    fat_total: Mapped[float] = mapped_column(default=0.0)
    fat_saturated: Mapped[float] = mapped_column(default=0.0)
    protein: Mapped[float] = mapped_column(default=0.0)
    sodium: Mapped[float] = mapped_column(default=0.0)
    potassium: Mapped[float] = mapped_column(default=0.0)
    cholesterol: Mapped[float] = mapped_column(default=0.0)
    carbohydrates_total: Mapped[float] = mapped_column(default=0.0)
    fiber: Mapped[float] = mapped_column(default=0.0)
    sugar: Mapped[float] = mapped_column(default=0.0)

    # Relationships
    ingredient_items: Mapped[List["IngredientItem"]] = relationship(
        back_populates="ingredient"
    )

    def __repr__(self):
        return f"Ingredient {self.name} with an ID of {self.id}"




# Currently SQLAlchemy does not support async event handling,
# thats why setting nutritional values is currently done in the Background Tasks
# @listens_for(Ingredient, "before_insert")
# async def set_nutritional_values(mapper, connection, target):
#     client = NutritionalAPIClient()
#     nutrition_data = await client.get_nutritional_values(target)
#     for key, value in nutrition_data.items():
#         if key.find("_") >= 0:
#             key = "_".join(key.split("_")[:-1])
#         target.__setattr__(key, value)


class Dish(Base):
    __tablename__ = "dish"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    recipe: Mapped[str | None] = mapped_column(Text)

    ingredients: Mapped[List["IngredientItem"]] = relationship(
        back_populates="dish"
    )


class IngredientItem(Base):
    """
    Proxy between Ingredient and Dish, allowing us to set amount of produce for each dish.
    Amount is in grams.
    """
    __tablename__ = "ingredientitem"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column()

    ingredient_id: Mapped[int | None] = mapped_column(ForeignKey("ingredient.id"))
    ingredient: Mapped["Ingredient | None"] = relationship(
        back_populates="ingredient_items"
    )

    dish_id: Mapped[int | None] = mapped_column(ForeignKey("dish.id"))
    dish: Mapped["Dish | None"] = relationship(
        back_populates="ingredients"
    )