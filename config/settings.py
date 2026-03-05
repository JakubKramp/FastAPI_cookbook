import environ

from core.constants import FILE_UPLOADER_CLASSES

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
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
PLAYWRIGHT_ENABLED = env.bool("PLAYWRIGHT_ENABLED", default=False)

CLOUD_PROVIDER = env.str("CLOUD_PROVIDER")

# GCLOUD
GCLOUD_KEY_FILE = env.str("GCLOUD_KEY_FILE")
GCLOUD_BUCKET_NAME = env.str("GCLOUD_BUCKET_NAME")


# STORAGE
FILE_MAX_UPLOAD_SIZE = env.int("FILE_MAX_UPLOAD_SIZE")
ALLOWED_EXTENSIONS = env.list("ALLOWED_EXTENSIONS")

FILE_UPLOADER_CLASS = FILE_UPLOADER_CLASSES.get(CLOUD_PROVIDER, None)
