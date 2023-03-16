from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy import select
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
    if not ingredients:
        raise HTTPException(status_code=404, detail="Ingredient not found")
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
def delete_user(ingredient_id: int, session: Session = Depends(get_session)):
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(ingredient)
    session.commit()
    return {f"Ingredient {ingredient_id} deleted"}


@ingredient_router.post("/recipe/")
def crate_recipe(dish_data: CreateDish, session: Session = Depends(get_session)):
    dish_data = dish_data.dict()
    ingredients = dish_data.pop("ingredients")
    # dish = Dish(**dish_data)
    # session.add(dish)
    # session.commit()
    ingredient_items = []
    for ingredient in ingredients:
        i = session.exec(
            select(Ingredient).where(
                Ingredient.name == ingredient["ingredient"]["name"]
            )
        )
        print(i)
        # IngredientItem()
    # ingredients = [IngredientItem(**ingredient) for ingredient in ingredients]
    return "Siema"
