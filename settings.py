from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Settings."""

    metric_port: int = Field(env='METRIC_PORT', default=8000)
    mongodb_host: str = Field(env='MONGODB_HOST', default='mongodb')
    mongodb_port: str = Field(env='MONGODB_PORT', default='27017')
    mongodb_name: str = Field(env='MONGODB_NAME', default='air-watcher')
    mongodb_username: str = Field(env='MONGODB_USERNAME', default='username')
    mongodb_password: str = Field(env='MONGODB_PASSWORD', default='password')


settings = Settings()
