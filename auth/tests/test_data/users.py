create_user ={
                "email": "jeff.spicoli@labeouf.com",
                "username": "jeffS",
            }
update_user = {
                "email": "jeff.spicoli@labeouf.com",
                "password": "hewillnotdivideus",
                "username": "jeffS",
            }

profile = {
                "sex": "Male",
                "age": 30,
                "height": 180,
                "weight": 80,
                "activity_factor": "Little/no exercise",
                "smoking": True,
}
dri_data =       {
                "calories": 2500,
                "carbohydrates": 400,
                "fat": 300,
                "protein": 250,
                "fiber": 40,
                "potassium": 1.3,
                "sodium": 6.9
}
profile_detail = profile.copy()
profile_detail.update(dri_data.copy())
user_detail = update_user.copy()
user_detail.update(profile.copy())