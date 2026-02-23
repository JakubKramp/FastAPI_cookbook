from pydantic import BaseModel


class UserList(BaseModel):
    email: str
    username: str

    class Config:
        schema_extra = {
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
        schema_extra = {
            "example": {
                "email": "jeff.spicoli@labeouf.com",
                "password": "hewillnotdivideus",
                "username": "jeffS",
            }
        }


class UserCreate(UserList):
    password: str | None

    class Config:
        schema_extra = {
            "example": {
                "email": "jeff.spicoli@labeouf.com",
                "password": "hewillnotdivideus",
                "username": "jeffS",
            }
        }



class UpdateProfile(BaseModel):
    sex: str | None
    activity_factor: str | None
    age: int | None
    height: int | None
    weight: int | None
    smoking: bool | None


class BaseProfile(BaseModel):
    sex: str
    activity_factor: str | None
    age: int
    height: int
    weight: int
    smoking: bool

    class Config:
        schema_extra = {
            "example": {
                "sex": "male",
                "age": 30,
                "height": 180,
                "weight": 80,
                "activity_factor": "Little/no exercise",
                "smoking": True,
            }
        }



class DietaryReferenceIntakes(BaseModel):
    calories: int | None
    carbohydrates: int | None
    fat: int | None
    protein: int | None
    fiber: int | None
    potassium: int | None
    sodium: int | None

class ProfileDetail(BaseProfile):
    DRI: DietaryReferenceIntakes

    class Config:
        schema_extra = {
            "example": {
                "sex": "male",
                "age": 30,
                "height": 180,
                "weight": 80,
                "activity_factor": "Little/no exercise",
                "smoking": True,
                'DRI':{
                    'calories': 4000,
                    'carbohydrates': 4000,
                    'fat': 4000,
                    'protein': 4000,
                    'fiber': 4000,
                    'potassium': 4000,
                    'sodium': 4000,
                }
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
