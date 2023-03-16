from pydantic import BaseSettings


class AuthConfig(BaseSettings):
    JWT_ALG: str
    JWT_EXP: int = 5  # minutes
    JWT_SECRET: str
    JWT_EXTRA_SECRET: str

    REFRESH_TOKEN_KEY: str = "refreshToken"
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days

    SECURE_COOKIES: bool = True
    SITE_DOMAIN: str

    SENDER_EMAIL: str
    SENDER_EMAIL_PASSWORD: str


auth_config = AuthConfig()
