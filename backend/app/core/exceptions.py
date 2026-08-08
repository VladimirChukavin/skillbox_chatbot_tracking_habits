class AppException(Exception):
    status_code: int
    error_type: str
    error_message: str

    def __init__(self, error_message: str | None = None) -> None:
        if error_message is not None:
            self.error_message = error_message
        super().__init__(self.error_message)


class AuthenticationError(AppException):
    status_code = 401
    error_type = "authentication_error"
    error_message = "Authentication failed"


class ValidationError(AppException):
    status_code = 400
    error_type = "validation_error"
    error_message = "Validation failed"


class NotFoundError(AppException):
    status_code = 404
    error_type = "not_found"
    error_message = "Entity not found"


class ForbiddenError(AppException):
    status_code = 403
    error_type = "forbidden"
    error_message = "Access denied"


class ConflictError(AppException):
    status_code = 409
    error_type = "conflict_error"
    error_message = "Conflict"
