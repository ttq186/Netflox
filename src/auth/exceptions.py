from src.auth.constants import ErrorMessage
from src.exceptions import BadRequest, NotAuthenticated, PermissionDenied


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorMessage.AUTHENTICATION_REQUIRED


class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorMessage.AUTHORIZATION_FAILED


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorMessage.INVALID_TOKEN


class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorMessage.INVALID_CREDENTIALS


class EmailTaken(BadRequest):
    DETAIL = ErrorMessage.EMAIL_TAKEN


class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = ErrorMessage.REFRESH_TOKEN_NOT_VALID
