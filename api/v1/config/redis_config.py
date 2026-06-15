from pydantic_settings import BaseSettings


class Settings(BaseSettings): 
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_USERNAME: str | None = None
    REDIS_PASSWORD: str | None = None


    

settings = Settings()