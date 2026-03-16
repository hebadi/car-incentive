from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/incentive_drive"
    redis_url: str = "redis://localhost:6379/0"
    api_secret_key: str = "change-me-in-production"

    marketcheck_api_key: str = ""
    anthropic_api_key: str = ""
    gemini_api_key: str = ""
    trustedform_api_key: str = ""
    sendgrid_api_key: str = ""
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
