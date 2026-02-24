from pydantic import BaseModel

from auth.constants import SexEnum


class UserList(BaseModel):
    email: str
    username: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "jeff.spicoli@labeouf.com",
                "username": "jeffS",
            }
        }

class UserUpdate(BaseModel):
    """
    This does not inherit from UserList intentionally, because email and username are nullable here.
    """
    email: str | None
    username: str | None
    password: str | None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "jeff.spicoli@labeouf.com",
                "password": "hewillnotdivideus",
                "username": "jeffS",
            }
        }


class UserCreate(UserList):
    password: str | None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "jeff.spicoli@labeouf.com",
                "password": "hewillnotdivideus",
                "username": "jeffS",
            }
        }



class UpdateProfile(BaseModel):
    sex: SexEnum | None = None
    activity_factor: str | None = None
    age: int | None = None
    height: int | None = None
    weight: int | None = None
    smoking: bool | None = None


class BaseProfile(BaseModel):
    sex: SexEnum
    activity_factor: str | None
    age: int
    height: int
    weight: int
    smoking: bool

    class Config:
        json_schema_extra = {
            "example": {
                "sex": "Male",
                "age": 30,
                "height": 180,
                "weight": 80,
                "activity_factor": "Little/no exercise",
                "smoking": True,
            }
        }



class DietaryReferenceIntakes(BaseModel):
    calories: float | None
    carbohydrates: float | None
    fat: float | None
    protein: float | None
    fiber: float | None
    potassium: float | None
    sodium: float | None

class ProfileDetail(BaseProfile):
    calories: float | None = None
    carbohydrates: float | None = None
    fat: float | None = None
    protein: float | None = None
    fiber: float | None = None
    potassium: float | None = None
    sodium: float | None = None


    class Config:
        json_schema_extra = {
            "example": {
                "sex": "Male",
                "age": 30,
                "height": 180,
                "weight": 80,
                "activity_factor": "Little/no exercise",
                "smoking": True,
                'calories': 4000,
                'carbohydrates': 4000,
                'fat': 4000,
                'protein': 4000,
                'fiber': 4000,
                'potassium': 4000,
                'sodium': 4000,
            }
        }

class UserDetail(UserList):
    id: int
    profile: ProfileDetail | None

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
