from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine

from auth.routes import user_router
from config import settings
from fridge.routes import fridge_router
from recipes.routes import ingredient_router

engine = create_async_engine(settings.DATABASE_URL)


app = FastAPI()


@app.get("/health", status_code=200)
async def health_check():
    return {"server_status": "ok"}




app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [fridge_router, user_router, ingredient_router]

for router in routers:
    app.include_router(router)
