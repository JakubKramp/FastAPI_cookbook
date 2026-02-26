from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, Response

from app.utils.db import get_session
from recipes.models import (
    Dish,
    Ingredient,
    IngredientItem,
)
from recipes.nutritional_data import NutritionalAPIClient
from recipes.schemas import (
    CreateDish,
    CreateIngredient,
    DishDetail,
    ListDish,
    ListIngredient,
    NutritionalValues,
    UpdateIngredient,
)

ingredient_router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@ingredient_router.post("/", response_model=ListIngredient, status_code=201)
async def create_ingredient(
    ingredient: CreateIngredient,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    result = await session.scalar(select(Ingredient).where(Ingredient.name == ingredient.name.lower()))
    if result:
        await session.refresh(result)
        return result
    else:
        db_ingredient = Ingredient(**ingredient.model_dump())
        session.add(db_ingredient)
        await session.commit()
        await session.refresh(db_ingredient)
        nutri_client = NutritionalAPIClient()
        background_tasks.add_task(nutri_client.fill_nutritional_values, db_ingredient, session)
        return db_ingredient


@ingredient_router.get("/{ingredient_id}", response_model=ListIngredient, status_code=200)
async def ingredient_detail(ingredient_id: int, session: AsyncSession = Depends(get_session)):
    ingredient = await session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@ingredient_router.get("/", response_model=list[ListIngredient], status_code=200)
async def ingredient_list(session: AsyncSession = Depends(get_session)):
    result = await session.scalars(select(Ingredient))
    ingredients = result.all()
    return ingredients



@ingredient_router.patch("/{ingredient_id}", response_model=ListIngredient, status_code=200)
async def update_ingredient(
    ingredient_id: int,
    ingredient_data: UpdateIngredient,
    session: AsyncSession = Depends(get_session),
):

    ingredient = await session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    ingredient_data = ingredient_data.model_dump(exclude_unset=True)
    for key, value in ingredient_data.items():
        setattr(ingredient, key, value)
    session.add(ingredient)
    await session.commit()
    await session.refresh(ingredient)
    return ingredient


@ingredient_router.delete("/{ingredient_id}", status_code=204)
async def delete_ingredient(ingredient_id: int, session: AsyncSession = Depends(get_session)):
    ingredient = await session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    await session.delete(ingredient)
    await session.commit()
    return Response(content='', status_code=204)


@ingredient_router.post(
    "/dish/",
    response_model=DishDetail,
    status_code=201,
    summary="Create a dish",
    response_description="Created dish",
)
async def create_dish(dish_data: CreateDish, session: AsyncSession = Depends(get_session)):
    dish_dict = dish_data.model_dump()
    ingredients = dish_dict.pop("ingredients")

    dish = Dish(**dish_dict)
    session.add(dish)
    await session.flush()

    existing = await session.scalars(
        select(Ingredient).where(Ingredient.name.in_([i['name'] for i in ingredients]))
    )
    existing_ingredients = {i.name: i for i in existing.all()}

    # bulk create missing ingredients
    new_ingredients = [
        Ingredient(name=i['name'])
        for i in ingredients
        if i['name'] not in existing_ingredients
    ]
    if new_ingredients:
        session.add_all(new_ingredients)
        await session.flush()
        existing_ingredients.update({i.name: i for i in new_ingredients})

    # bulk create ingredient items
    session.add_all([
        IngredientItem(
            dish_id=dish.id,
            ingredient_id=existing_ingredients[i['name']].id,
            amount=i['amount']
        )
        for i in ingredients
    ])

    await session.commit()
    await session.refresh(dish)
    return dish

@ingredient_router.get("/dish/", response_model=list[ListDish], status_code=200)
async def dish_list(session: AsyncSession = Depends(get_session)):
    result = await session.scalars(select(Dish))
    dishes = result.all()
    return dishes


@ingredient_router.delete("/dish/{dish_id}", status_code=204)
async def delete_dish(dish_id: int, session: AsyncSession = Depends(get_session)):
    dish = await session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    await session.delete(dish)
    await session.commit()
    return JSONResponse(content="", status_code=204)


@ingredient_router.get("/dish/{dish_id}", response_model=DishDetail, status_code=200)
async def dish_detail(dish_id: int, session: AsyncSession = Depends(get_session)):
    dish = await session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    nut_values = list(NutritionalValues.model_fields.keys())
    nut_expressions = [
        func.sum(getattr(Ingredient, param) * IngredientItem.amount / 100).label(param)
        for param in nut_values
    ]

    nut_query = await session.execute(
        select(*nut_expressions)
        .join(IngredientItem, Ingredient.id == IngredientItem.ingredient_id)
        .where(IngredientItem.dish_id == dish_id)
        .group_by(IngredientItem.dish_id)
    )
    nut_row = nut_query.first()

    return {
        **dish.__dict__,
        "nutritional_values": dict(zip(nut_values, nut_row)) if nut_row else None,
    }