from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://queue:queue@localhost:5432/queue"
    poll_interval_seconds: float = 0.5
    lease_seconds: int = 15
    processing_seconds: float = 10
    max_attempts: int = 4

    model_config = SettingsConfigDict(env_prefix="QUEUE_")
