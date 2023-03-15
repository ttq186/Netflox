from enum import Enum


class ErrorMessage:
    AUTHENTICATION_REQUIRED = "Authentication required!"
    AUTHORIZATION_FAILED = "Authorization failed. User has no access."
    INVALID_TOKEN = "Invalid token!"
    INVALID_CREDENTIALS = "Invalid credentials!"
    EMAIL_TAKEN = "Email is already taken."
    REFRESH_TOKEN_NOT_VALID = "Refresh token is not valid."
    REFRESH_TOKEN_REQUIRED = "Refresh token is required either in the body or cookie!"


class AuthMethod(str, Enum):
    NORMAL = "NORMAL"
    THIRD_PARY = "THIRD_PARTY"
