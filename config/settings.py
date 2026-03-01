import environ

env = environ.Env()
environ.Env.read_env()

# Database

DATABASE_URL = f"postgresql+asyncpg://{env.str('POSTGRES_USER')}:{env.str('POSTGRES_PASSWORD')}@{env.str('POSTGRES_HOST')}/{env.str('POSTGRES_DATABASE')}"
TEST_DATABASE_URL = f"postgresql+asyncpg://{env.str('POSTGRES_USER')}:{env.str('POSTGRES_PASSWORD')}@{env.str('POSTGRES_HOST')}/test_db"

# External APIs

NUTRITION_API_URL = f"{env.str('NUTRITION_API_URL')}"
NUTRITION_APIKEY = f"{env.str('NUTRITION_APIKEY')}"

# Cryptography

ALGORITHM = env.str("ALGORITHM")
SECRET_KEY = env.str("SECRET_KEY")

# Celery
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")

# App Behavior
ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=60)
APP_LOCATION = env.str("APP_LOCATION")
PLAYWRIGHT_ENABLED = env.bool("PLAYWRIGHT_ENABLED", default=False)
