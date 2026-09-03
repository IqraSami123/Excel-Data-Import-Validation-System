# centerlized point for the all configurations of project
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str      

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",     #to ignore the other variables in the .env file, that we dont need 
    )


settings = Settings()