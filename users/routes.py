from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlmodel import Session, create_engine
from passlib.context import CryptContext

from config import settings
from users.models import User, UserDetail

engine = create_engine(settings.DATABASE_URL, echo=True)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_session():
    with Session(engine) as session:
        yield session


user_router = APIRouter(prefix="/user", tags=["users"])


@user_router.post("/", response_model=UserDetail, status_code=201)
def sign_up(user: UserDetail, session: Session = Depends(get_session)):
    user = User.from_orm(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@user_router.get("/", response_model=UserDetail, status_code=200)
def user_detail(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.patch("/", response_model=UserDetail)
def update_user(
    user_id: int, user_data: UserDetail, session: Session = Depends(get_session)
):
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


@user_router.delete("/")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {f"User {user_id} deleted"}


@user_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}
