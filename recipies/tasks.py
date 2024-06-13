import httpx

from config import settings


async def get_nutritional_values(ingredient, session):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.NUTRITION_API_URL,
            params={"query": ingredient.name},
            headers={"X-Api-Key": settings.NUTRITION_APIKEY},
        )
        nutrition_data = response.json()[0]
        nutrition_data.pop("name", None)
        nutrition_data.pop("serving_size_g", None)
        for key, value in nutrition_data.items():
            if key.find("_") >= 0:
                key = "_".join(key.split("_")[:-1])
            ingredient.__setattr__(key, value)
        session.add(ingredient)
        session.commit()
