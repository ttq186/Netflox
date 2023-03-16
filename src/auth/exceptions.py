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


class EmailNotRegistered(BadRequest):
    DETAIL = ErrorMessage.EMAIL_NOT_REGISTERED


class AccountSuspended(PermissionDenied):
    DETAIL = ErrorMessage.ACCOUNT_SUSPENDED


class AccountNotActivated(PermissionDenied):
    DETAIL = ErrorMessage.ACCOUNT_NOT_ACTIVATED
