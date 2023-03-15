from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlmodel import Session, create_engine
from config import settings
from recipies.models import CreateIngredient, Ingredient
from users.models import User, UserDetail

ingredient_router = APIRouter(prefix='/ingredient', tags=['ingredients'])

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


@ingredient_router.get("/", response_model=Ingredient)
def ingredient_detail(ingredient_id: int, session: Session = Depends(get_session)):
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

"""
@user_router.patch("/", response_model=UserDetail)
def update_user(user_id: int, user_data: UserDetail, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user_data.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@user_router.delete('/')
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {f"User {user_id} deleted"}
"""