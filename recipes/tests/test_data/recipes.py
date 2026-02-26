nutritional_values = {
                "calories": 34,
                "fat_total": 0.2,
                "protein": 0.8,
                "sodium": 57,
                "potassium": 30,
                "fiber": 3,
                "carbohydrates_total": 8.3,
                "sugar": 3.4,
            }
example_ingredient = nutritional_values.copy()
example_ingredient.update({'name': 'carrot'})

example_create_ingredient_item = {'name': 'carrot', 'amount': 1000}
example_list_dish = {
                "id": 140,
                "name": "Mashed potatoes",
                "recipe": "Mash the potatoes along with the butter. Eat the mashed potatoes",
                "ingredients": [{"amount": 700, "name": "potato"}, {"amount": 300, "name": "butter"}],
            }

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

example_dish_detail = example_create_dish.copy()
example_dish_detail.update({'id':140})