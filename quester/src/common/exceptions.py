from common.logger import get_logger
from config import Settings, get_settings

settings: Settings = get_settings()
# logger = get_logger(__name__)
logger = get_logger(__name__, log_type="json")


class QuesterBaseError(Exception):
    """
    Base QuesterBaseError

    Use a base Quester error - so that one common handler
    can be used for all Quester errors
    """

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        self.message = "QuesterError"
        self.status_code = (400,)


class QuesterBadRequestError(QuesterBaseError):
    def __init__(
        self,
        message: str = "Client-side error",
    ) -> None:
        self.status_code = (400,)
        super().__init__(message)


class QuesterInternalServerError(QuesterBaseError):
    def __init__(
        self,
        message: str = "Server-side error",
    ) -> None:
        self.status_code = (500,)
        super().__init__(message)


class QuesterAWSClientError(QuesterBaseError):
    def __init__(
        self,
        message: str = "Error connecting to AWS service",
    ) -> None:
        self.status_code = (500,)
        super().__init__(message)


class QuesterDBConnectionError(QuesterBaseError):
    def __init__(
        self,
        message: str = "Error connecting to Database",
    ) -> None:
        self.status_code = (500,)
        super().__init__(message)
