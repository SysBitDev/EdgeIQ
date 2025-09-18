import os

from pydantic import BaseModel


class Settings(BaseModel):
    APP_NAME: str = "EdgeIQ Ingest API"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/edgeiq"
    )


settings = Settings()
