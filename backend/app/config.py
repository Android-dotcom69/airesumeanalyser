from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_api_key: str
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "career_guidance"
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    frontend_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()
