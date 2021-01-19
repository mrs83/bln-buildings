import os
from envparse import env


PROJECT_NAME = env.str("PROJECT_NAME", default="bln-buildings")
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
API_V1_STR = env.str("API_V1_STR", default="/api/v1")
SECRET_KEY = env.str("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
ACCESS_TOKEN_ALGORITHM = env.str("ACCESS_TOKEN_ALGORITHM", default="HS256")
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default="redis://redis:6379/0")
