from datetime import date

example_product = {
    "name": "carrot",
    "amount": 100,
    "expires_on": "2026-12-31",
    "fridge_id": 1,
}
example_db_product = {
    "name": "carrot",
    "amount": 100,
    "expires_on": date(year=2020, month=12, day=12),
    "fridge_id": 1,
}
example_fridge = {"products": [example_product]}
example_ingredient = {
    "name": "carrot",
    "calories": 34.0,
    "fat_total": 0.2,
    "fat_saturated": 0.0,
    "protein": 0.8,
    "sodium": 57.0,
    "potassium": 30.0,
    "carbohydrates_total": 8.3,
    "fiber": 3.0,
    "sugar": 3.4,
}
example_ingredient_api_response = [
    {
        "calories": 34,
        "fat_total_g": 0.2,
        "fat_saturated_g": 0,
        "protein_g": 0.8,
        "sodium_mg": 57,
        "potassium_mg": 30,
        "carbohydrates_total_g": 8.3,
        "fiber_g": 3,
        "sugar_g": 3.4,
    }
]
example_create_dish = {
    "name": "Mashed potatoes",
    "recipe": "Mash the potatoes along with the butter. Eat the mashed potatoes",
    "ingredients": [{"amount": 700, "name": "potato"}, {"amount": 300, "name": "butter"}],
    "nutritional_values": {
        "calories": 3339,
        "fat_total": 315.04,
        "protein": 27.23,
        "sodium": 1533,
        "potassium": 1533,
        "fiber": 10.5,
        "carbohydrates_total": 94.43,
        "sugar": 10.36,
    },
}
