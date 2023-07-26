from fastapi import Request, Response, status

from common.exceptions import QuesterBaseError
from common.logger import get_logger

logger = get_logger(__name__)

"""This file is a not referenced anywhere. 

It's just a placeholder for future usage. As of now there's no need to add 
custom exception handlers, all the custom exceptions will lead to raising 
HTTPExceptions which are getting handled by the default FastApi handlers
"""


def quester_exception_handler(request: Request, exc: QuesterBaseError):
    """
    quester common exception handler

    based on the status_code set, handles specific Quester exception
    """
    if exc.status_code == 400:
        logger.error(f"Bad request: {request.url}")
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    if exc.status_code == 500:
        logger.error(
            f"Internal Server Error.  \
            Please contact your administrator with the complete error \
             message so that it can be investigated: {request.url}"
        )
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
