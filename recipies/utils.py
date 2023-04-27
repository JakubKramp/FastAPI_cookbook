import requests

from config import settings


class NutritionalAPIClient:
    apikey = settings.NUTRITION_APIKEY

    def get_nutritional_values(self, ingredient):
        response = requests.get(
            settings.NUTRITION_API_URL,
            params={"query": ingredient.name},
            headers={"X-Api-Key": self.apikey},
        )
        nutrition_data = response.json()[0]
        nutrition_data.pop("name", None)
        nutrition_data.pop("serving_size_g", None)
        return nutrition_data
