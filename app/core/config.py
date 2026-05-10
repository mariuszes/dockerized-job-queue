import os
from dotenv import load_dotenv

load_dotenv()


def get_env_value(name: str) -> str:
    value = os.getenv(name)

    if value is None:
        raise RuntimeError(f"Missing environment variable: {name}")

    return value


POSTGRES_USER = get_env_value("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_value("POSTGRES_PASSWORD")
POSTGRES_HOST = get_env_value("POSTGRES_HOST")
POSTGRES_PORT = get_env_value("POSTGRES_PORT")
POSTGRES_DB = get_env_value("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)