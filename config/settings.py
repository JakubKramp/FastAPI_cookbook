import environ

env = environ.Env()
environ.Env.read_env()

DATABASE_URL = f"postgresql://{env.str('POSTGRES_USER')}:{env.str('POSTGRES_PASSWORD')}@{env.str('POSTGRES_HOST')}/{env.str('POSTGRES_DATABASE')}"
NUTRITION_API_URL = f"{env.str('NUTRITION_API_URL')}"
NUTRITION_APIKEY = f"{env.str('NUTRITION_APIKEY')}"