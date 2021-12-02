from fastapi import HTTPException, status

class Exception:

    @classmethod
    def forbidden_access(cls):
        return HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Incorrect username or password",
            headers = { "WWW-Authenticate": "Bearer" },
        )

    @classmethod
    def unauthorized_access(cls):
        return HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid token!",
            headers = { "WWW-Authenticate": "Bearer" },
        )

    @classmethod
    def resource_not_found(cls, message):
        return HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = message
        )