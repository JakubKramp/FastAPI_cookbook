from typing import List

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.db import Base


class Ingredient(Base):
    """
    Nutritional values by default refer to 100g serving.
    Relations:
    - IngredientItem(recipes) one to many
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
        back_populates="ingredient",
        lazy = 'selectin'
    )

    def __repr__(self):
        return f"Ingredient {self.name} with an ID of {self.id}"


class Dish(Base):
    """
    Model that represents a recipe
    Relations:
    - IngredientItem(recipes) one to many
    """
    __tablename__ = "dish"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    recipe: Mapped[str | None] = mapped_column(Text)

    ingredients: Mapped[List["IngredientItem"]] = relationship(
        back_populates="dish",
        lazy = 'selectin'
    )


class IngredientItem(Base):
    """
    Proxy between Ingredient and Dish, allowing us to set amount of produce for each dish.
    Amount is in grams.
        Relations:
    - Ingredient(recipes) many to one
    - Dish(ingredients) many to one
    """
    __tablename__ = "ingredientitem"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column()

    ingredient_id: Mapped[int | None] = mapped_column(ForeignKey("ingredient.id"))
    ingredient: Mapped["Ingredient | None"] = relationship(
        back_populates="ingredient_items",
        lazy = 'selectin'
    )

    dish_id: Mapped[int | None] = mapped_column(ForeignKey("dish.id"))
    dish: Mapped["Dish | None"] = relationship(
        back_populates="ingredients",
        lazy='selectin'
    )