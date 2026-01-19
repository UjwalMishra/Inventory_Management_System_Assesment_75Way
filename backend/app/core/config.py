from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str
    env: str

    # DB
    database_url: str
    
    # JWT
    jwt_secret: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
