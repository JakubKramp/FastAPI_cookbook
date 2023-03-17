from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy import func
from sqlmodel import Session, create_engine
from config import settings
from recipies.models import (
    CreateIngredient,
    Ingredient,
    ListIngredient,
    UpdateIngredient,
    CreateDish,
    Dish,
    IngredientItem,
    ListDish,
    DishDetail,
    NutritionalValues,
)

ingredient_router = APIRouter(prefix="/ingredient", tags=["ingredients"])

engine = create_engine(settings.DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


@ingredient_router.post("/", response_model=Ingredient)
def create(ingredient: CreateIngredient, session: Session = Depends(get_session)):
    ingredient = Ingredient.from_orm(ingredient)
    session.add(ingredient)
    session.commit()
    session.refresh(ingredient)
    return ingredient


@ingredient_router.get("/{ingredient_id}", response_model=Ingredient)
def ingredient_detail(ingredient_id: int, session: Session = Depends(get_session)):
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@ingredient_router.get("/", response_model=list[ListIngredient])
def ingredient_list(session: Session = Depends(get_session)):
    ingredients = session.scalars(select(Ingredient)).all()
    return ingredients


@ingredient_router.patch("/{ingredient_id}", response_model=Ingredient)
def update_ingredient(
    ingredient_id: int,
    ingredient_data: UpdateIngredient,
    session: Session = Depends(get_session),
):
    """
    Todo: Update SQLAlchemy Event to update the data.
    :param ingredient_id:
    :param ingredient_data:
    :param session:
    :return:
    """
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="User not found")
    ingredient_data = ingredient_data.dict(exclude_unset=True)
    for key, value in ingredient_data.items():
        setattr(ingredient, key, value)
    session.add(ingredient)
    session.commit()
    session.refresh(ingredient)
    return ingredient


@ingredient_router.delete("/{ingredient_id}")
def delete_ingredient(ingredient_id: int, session: Session = Depends(get_session)):
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(ingredient)
    session.commit()
    return {f"Ingredient {ingredient_id} deleted"}


@ingredient_router.post("/dish/", response_model=Dish)
def create_dish(dish_data: CreateDish, session: Session = Depends(get_session)):
    dish_data = dish_data.dict()
    ingredients = dish_data.pop("ingredients")
    dish = Dish(**dish_data)
    session.add(dish)
    session.commit()
    session.refresh(dish)
    ingredient_items = []
    for ingredient in ingredients:
        i = session.scalars(
            select(Ingredient).where(
                Ingredient.name == ingredient["ingredient"]["name"].lower()
            )
        ).first()
        if not i:
            i = Ingredient(name=ingredient["ingredient"]["name"].lower())
            session.add(i)
            session.commit()
        item = IngredientItem(ingredient=i, amount=ingredient["amount"], dish=dish)
        ingredient_items.append(item)
    session.bulk_save_objects(ingredient_items)
    session.add(dish)
    session.commit()
    session.refresh(dish)
    return dish


@ingredient_router.get("/dish/", response_model=list[ListDish])
def dish_list(session: Session = Depends(get_session)):
    dishes = session.scalars(select(Dish)).all()
    return dishes


@ingredient_router.delete("/dish/{dish_id}")
def delete_dish(dish_id: int, session: Session = Depends(get_session)):
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    session.delete(dish)
    session.commit()
    return {f"Dish {dish_id} deleted"}


@ingredient_router.get("/dish/{dish_id}", response_model=DishDetail)
def dish_detail(dish_id: int, session: Session = Depends(get_session)):
    nut_values = NutritionalValues.__fields__.keys()
    nut_expressions = [
        func.sum(getattr(Ingredient, param) * IngredientItem.amount / 100).label(param)
        for param in nut_values
    ]
    nut_query = (
        session.query(*nut_expressions)
        .join(IngredientItem, Ingredient.id == IngredientItem.ingredient_id)
        .filter(IngredientItem.dish_id == dish_id)
        .group_by(IngredientItem.dish_id)
        .first()
    )
    dish = session.get(Dish, dish_id)
    dish_dict = dish.dict()
    dish_dict["nutritional_values"] = {
        nut_value: value for nut_value, value in zip(nut_values, nut_query)
    }
    dish_dict["ingredients"] = dish.ingredients
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish_dict
