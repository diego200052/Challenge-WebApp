from pydantic_settings import BaseSettings
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    ACTUAL_TIMEZONE: str
    DEBUG: bool
    SECRET_KEY: str
    SECURITY_PASSWORD_SALT: str
    SECURITY_USER_IDENTITY_ATTRIBUTES: str
    CLIENT_ORIGIN: str
    API_URL: str

    class Config:
        env_file = "./.env"

    @property
    def timezone(self) -> ZoneInfo:
        return ZoneInfo(self.ACTUAL_TIMEZONE)


settings = Settings()
