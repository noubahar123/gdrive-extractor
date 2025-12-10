import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Image Import API"
    API_V1_STR: str = "/api/v1"

    # 🔴 For now, FORCE SQLite. Ignore DATABASE_URL from env.
    DATABASE_URL: str = "sqlite:///./image_import.db"

    # We can keep REDIS_URL from env for later.
    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )


settings = Settings()


# Changing DB to sqlLite
# class Settings:
#     PROJECT_NAME: str = "Image Import API"
#     API_V1_STR: str = "/api/v1"

#     DATABASE_URL: str = os.getenv(
#         "DATABASE_URL",
#         "postgresql://user:password@localhost:5432/image_import_db"
#     )

#     REDIS_URL: str = os.getenv(
#         "REDIS_URL",
#         "redis://localhost:6379/0"
#     )

# settings = Settings()
