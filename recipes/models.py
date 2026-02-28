from datetime import date
from typing import List

from sqlalchemy import Column, ForeignKey, String, Table, Text, UniqueConstraint, select
from sqlalchemy.ext.asyncio import AsyncSession
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
    carbohydrates_total: Mapped[float] = mapped_column(default=0.0)
    fiber: Mapped[float] = mapped_column(default=0.0)
    sugar: Mapped[float] = mapped_column(default=0.0)

    # Relationships
    ingredient_items: Mapped[List["IngredientItem"]] = relationship(
        back_populates="ingredient", lazy="selectin"
    )

    def __repr__(self):
        return f"Ingredient {self.name} with an ID of {self.id}"


dish_tag = Table(
    "dish_tag",
    Base.metadata,
    Column("dish_id", ForeignKey("dish.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


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

    ingredients: Mapped[List["IngredientItem"]] = relationship(back_populates="dish", lazy="selectin")
    tags: Mapped[list["Tag"]] = relationship(secondary=dish_tag, back_populates="dish", lazy="selectin")


class IngredientItem(Base):
    """
    Proxy between Ingredient and Dish, allowing us to set amount of produce for each dish.
    Amount is in grams.
        Relations:
    - Ingredient(recipes) many to one
    - Dish(recipes) many to one
    - Product(recipes) one to one
    """

    __tablename__ = "ingredientitem"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column()

    ingredient_id: Mapped[int | None] = mapped_column(ForeignKey("ingredient.id"))
    ingredient: Mapped["Ingredient | None"] = relationship(back_populates="ingredient_items", lazy="selectin")

    dish_id: Mapped[int | None] = mapped_column(ForeignKey("dish.id"))
    dish: Mapped["Dish | None"] = relationship(back_populates="ingredients", lazy="selectin")


class Product(Base):
    """
    Item with an amount and expiry date.
    Relations:
    - IngredientItem(recipes) many to one
    - Dish(ingredients) many to one
    """

    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredient.id"))
    ingredient: Mapped["Ingredient"] = relationship(lazy="selectin")
    amount: Mapped[int] = mapped_column()
    expires_on: Mapped[date] = mapped_column()
    marked_for_delete: Mapped[bool] = mapped_column(default=False)
    fridge_id: Mapped[int | None] = mapped_column(ForeignKey("fridge.id"))
    fridge: Mapped["Fridge"] = relationship(
        back_populates="products",
        lazy="selectin",
        uselist=True,
    )

    @property
    def name(self) -> str:
        return self.ingredient.name

    @name.setter
    def name(self, value: str) -> None:
        pass  # name is set via ingredient, ignore

    def is_expired(self) -> bool:
        return self.expires_on < date.today()

    @classmethod
    def expired(cls):
        return cls.marked_for_delete == True

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> "Product":
        name = kwargs.pop("name")
        ingredient = await session.scalar(select(Ingredient).where(Ingredient.name == name))
        if not ingredient:
            ingredient = Ingredient(name=name)
            session.add(ingredient)
            await session.flush()
        await session.refresh(ingredient)
        product = cls(**kwargs, ingredient=ingredient)
        session.add(product)
        await session.flush()
        return product


class Tag(Base):
    __tablename__ = "tag"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    dish: Mapped[List["Dish"]] = relationship(secondary=dish_tag, back_populates="tags", lazy="selectin")
