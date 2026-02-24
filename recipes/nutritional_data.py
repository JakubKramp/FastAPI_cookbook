from typing import Dict

import aiohttp

from config import settings
from recipes.constants import NUTRITIONAL_VALUES_MAPPING
from recipes.schemas import NutritionalValues


class NutritionalAPIClient:
    apikey = settings.NUTRITION_APIKEY
    base_url = settings.NUTRITION_API_URL


    async def construct_url(self, ingredient_name:str, endpoint: str = 'search') -> str:
        return ''.join([self.base_url, endpoint, f'query={ingredient_name}', f'api_key={self.apikey}'])

    async def search_for_ingredients(self, ingredient_name: str) -> Dict[str, str]:
        url = await self.construct_url(ingredient_name)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()

    async def extract_nutritional_values(self, ingredient_name: str) -> NutritionalValues:
        data = await self.search_for_ingredients(ingredient_name)
        nutri_data = {
            NUTRITIONAL_VALUES_MAPPING[nutrient['nutrientName']]: nutrient['value']
            for nutrient in data['foods'][0]['foodNutrients'] # type: ignore
        }
        return NutritionalValues(**nutri_data)
