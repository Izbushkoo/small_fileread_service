from typing import List

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    API_KEY: str
    WIX_API_KEY: str
    WIX_SITE_ID: str
    WIX_ACCOUNT_ID: str


settings = Settings()
