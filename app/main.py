from fastapi import FastAPI
from users.routes import user_router

app = FastAPI()

app.include_router(user_router)