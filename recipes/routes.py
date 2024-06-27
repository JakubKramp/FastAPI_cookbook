from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy import select
from sqlalchemy import func
from sqlmodel import Session
from starlette.responses import JSONResponse

from recipes.models import (
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
from app.utils.db import get_session
from recipes.tasks import get_nutritional_values

ingredient_router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@ingredient_router.post("/", response_model=Ingredient, status_code=201)
async def create_ingredient(
    ingredient: CreateIngredient,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    if session.query(Ingredient).filter_by(name=ingredient.name.lower()).first():
        return HTTPException(409, "Item with this name already exists")
    ingredient = Ingredient.from_orm(ingredient)
    background_tasks.add_task(get_nutritional_values, ingredient, session)
    return ingredient


@ingredient_router.get("/{ingredient_id}", response_model=Ingredient, status_code=200)
def ingredient_detail(ingredient_id: int, session: Session = Depends(get_session)):
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@ingredient_router.get("/", response_model=list[ListIngredient], status_code=200)
def ingredient_list(session: Session = Depends(get_session)):
    ingredients = session.scalars(select(Ingredient)).all()
    return ingredients


@ingredient_router.patch("/{ingredient_id}", response_model=Ingredient, status_code=200)
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


@ingredient_router.delete("/{ingredient_id}", status_code=204)
def delete_ingredient(ingredient_id: int, session: Session = Depends(get_session)):
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    session.delete(ingredient)
    session.commit()
    return JSONResponse(content={"message": f"Ingredient {ingredient_id} deleted"}, status_code=204)


@ingredient_router.post(
    "/dish/",
    response_model=Dish,
    status_code=201,
    summary="Create a dish",
    response_description="Created dish",
)
def create_dish(dish_data: CreateDish, session: Session = Depends(get_session)):
    """
    Create a dish, along with associated Ingredient Items.
    - **name**: Name of the dish
    - **recipe**: Steps to perform to create the dish.
    - **ingredients**: List of IngredientItems required for the dish
    """
    dish_data = dish_data.dict()
    ingredients = dish_data.pop("ingredients")
    dish = Dish(**dish_data)
    session.add(dish)
    session.commit()
    session.refresh(dish)
    for ingredient in ingredients:
        i = session.scalars(
            select(Ingredient).where(Ingredient.name == ingredient["ingredient"]["name"].lower())
        ).first()
        if not i:
            i = Ingredient(name=ingredient["ingredient"]["name"].lower())
            session.add(i)
            session.commit()
        item = IngredientItem(ingredient=i, amount=ingredient["amount"], dish=dish)
        session.add(item)
        session.commit()
    session.add(dish)
    session.commit()
    session.refresh(dish)
    return dish


@ingredient_router.get("/dish/", response_model=list[ListDish], status_code=200)
def dish_list(session: Session = Depends(get_session)):
    dishes = session.scalars(select(Dish)).all()
    return dishes


@ingredient_router.delete("/dish/{dish_id}", status_code=204)
def delete_dish(dish_id: int, session: Session = Depends(get_session)):
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    session.delete(dish)
    session.commit()
    return JSONResponse(content={"message": f"Dish {dish_id} deleted"}, status_code=204)


@ingredient_router.get("/dish/{dish_id}", response_model=DishDetail, status_code=200)
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
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    else:
        dish_dict = dish.dict()
        dish_dict["nutritional_values"] = {
            nut_value: value for nut_value, value in zip(nut_values, nut_query)
        }
        dish_dict["ingredients"] = dish.ingredients
    return dish_dict
