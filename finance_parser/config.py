from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator

class Settings(BaseSettings):

    interval = 60  # The following values are supported: 1min, 5min, 15min, 30min, 60min
    api_key = "IH86CDCM2IPISXQ1"
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_USER: str = "finance_user"
    POSTGRES_PASSWORD: str = "finance_pass"
    POSTGRES_DB: str = "finance_db"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

settings = Settings()
