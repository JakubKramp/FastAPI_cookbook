example_ingredient = {
    "name": "carrot",
    "calories": 34.0,
    "fat_total": 0.2,
    "fat_saturated": 0.0,
    "protein": 0.8,
    "sodium": 57.0,
    "potassium": 30.0,
    "cholesterol": 0.0,
    "carbohydrates_total": 8.3,
    "fiber": 3.0,
    "sugar": 3.4,
}
example_ingredient_api_response = [
    {
        "name": "carrot",
        "calories": 34,
        "serving_size_g": 100,
        "fat_total_g": 0.2,
        "fat_saturated_g": 0,
        "protein_g": 0.8,
        "sodium_mg": 57,
        "potassium_mg": 30,
        "cholesterol_mg": 0,
        "carbohydrates_total_g": 8.3,
        "fiber_g": 3,
        "sugar_g": 3.4,
    }
]
example_create_dish = {
    "name": "Mashed potatoes",
    "recipe": "Mash the potatoes along with the butter. Eat the mashed potatoes",
    "ingredients": [
        {
            "amount": 700,
            "ingredient": {"name": "potato"},
        },
        {
            "amount": 300,
            "ingredient": {"name": "butter"},
        },
    ],
}
