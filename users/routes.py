from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, create_engine, SQLModel

from config import settings
from users.models import User, UserDetail

engine = create_engine(settings.DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
user_router = APIRouter(prefix='/user', tags=['users'])


@user_router.post("/", response_model=UserDetail)
def sign_up(user: UserDetail, session: Session = Depends(get_session)):
    user = User.from_orm(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@user_router.get("/", response_model=UserDetail)
def user_detail(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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
