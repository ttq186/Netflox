from typing import Any

from src.auth.config import auth_config


def get_refresh_token_settings(
    refresh_token: str | None = None,
    expired: bool = False,
) -> dict[str, Any]:
    base_cookie = {
        "key": auth_config.REFRESH_TOKEN_KEY,
        "httponly": True,
        "samesite": "none",
        "secure": auth_config.SECURE_COOKIES,
        "domain": auth_config.SITE_DOMAIN,
    }
    if expired or not refresh_token:
        return base_cookie

    return {
        **base_cookie,
        "value": refresh_token,
        "max_age": auth_config.REFRESH_TOKEN_EXP,
    }
