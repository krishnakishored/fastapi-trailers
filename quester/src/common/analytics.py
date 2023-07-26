import json
import time
from contextlib import asynccontextmanager, contextmanager
from dataclasses import asdict, dataclass, field
from functools import wraps

from common.logger import get_logger

logger = get_logger(__name__, log_type="json")


@dataclass(init=True, repr=True, frozen=True)
class QuesterAnalyticsRequest:
    """Creates the request object used by analytics service

    The request and response logs are paired together by transaction_id
    """

    msg_type: str = "request"
    transaction_id: str = "0123456789"  # transaction-id
    method: str = "GET"
    path: str = "/status"
    api_key: str = "NOAPIKEY"
    query_params: dict = field(default_factory=dict)
    level: str = "info"  # field used for the analytics mapping

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


@dataclass(init=True, repr=True, frozen=True)
class QuesterAnalyticsResponse:
    """Creates the response object used by analytics services

    The request and response logs are paired together by transaction_id
    """

    msg_type: str = "response"
    transaction_id: str = "0123456789"  # transaction-id
    method: str = "GET"
    path: str = "/status"
    status: int = 200  # HTTP STATUS_CODE
    latency: float = 0.0
    level: str = "info"  # field used for the analytics mapping

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    # def __str__(self) -> str:
    #     """Formats the object data members as a json string
    #     This format is used by elastic-search+kibana stack
    #     to analyse the usage logs.
    #     CAUTION: Changing the key names might break the monitoring pipelines
    #     """
    #     json_formatted_string = (
    #         f"{{"
    #         f'"level":"info",'  # field used for the analytics mapping
    #         f'"type":"{self.msg_type}",'
    #         f'"id":"{self.transaction_id}",'
    #         f'"method":"{self.method}",'
    #         f'"path":"{self.path}",'
    #         f'"status":"{self.status}",'
    #         f'"latency":"{self.latency:.6f}"'
    #         f"}}"
    #     )
    #     return json_formatted_string


@dataclass(init=True, repr=True, frozen=True)
class QuesterCodeFlow:
    msg_type: str = "codeflow"
    # transaction_id: str = "0123456789"  # transaction-id
    message: str = "text"
    module: str = __name__
    level: str = "debug"  # field used for the analytics mapping

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


@dataclass(init=True, repr=True, frozen=True)
class QuesterTimer(QuesterCodeFlow):
    """To log the messages related to codeflow/latency - for debugging"""

    latency: float = 0.000000


@contextmanager
def timing_context(code_block_desc: str = "", module_name: str = ""):
    """Calculate the time for the processing a block of code
    Args:
        code_block_desc (str): description of the code block
    """
    start_ts = time.perf_counter()
    try:
        yield
    finally:
        latency = time.perf_counter() - start_ts
        # func_name = inspect.stack()[1].function // get calling function name
        json_formatted_string = (
            f"{{"
            f'"code_block":"{code_block_desc}",'
            f'"module":"{module_name}",'
            f'"latency":"{latency:.6f}"'
            f"}}"
        )

        logger.debug(json_formatted_string)
        # logger.debug(
        #     f"processing_time for code_block: {code_block_desc} - {latency:.6f} seconds"
        # )


@asynccontextmanager
async def async_timing_context(code_block_desc: str = "", module_name: str = ""):
    """Calculate the time for the processing a block of code
    Args:
        code_block_desc (str): description of the code block
    """
    start_ts = time.perf_counter()
    try:
        yield
    finally:
        latency = time.perf_counter() - start_ts
        # func_name = inspect.stack()[1].function // get calling function name
        json_formatted_string = (
            f"{{"
            f'"code_block":"{code_block_desc}",'
            f'"module":"{module_name}",'
            f'"latency":"{latency:.6f}"'
            f"}}"
        )
        logger.debug(json_formatted_string)


# If analytics_decorator() has been called without arguments, the decorated function will be passed in as func.
# If it has been called with arguments, then func will be None,
# and some of the keyword arguments may have been changed from their default values.
# The * in the argument list means that the remaining arguments can’t be called as positional arguments.
def analytics_decorator(func=None, *, msg_type: str = "timer", msg_text: str = ""):
    """
    adds the json loggging to be caputured by kibana for analytics
    """

    def sub_decorator_analytics(func):
        ##  when a decorator uses arguments, you need to add an extra outer function.
        @wraps(func)
        def wrapper_analytics(*args, **kwargs):
            start_time = time.perf_counter()
            value = func(*args, **kwargs)
            end_time = time.perf_counter()
            latency: float = round(end_time - start_time, 6)
            # default to function name if msg_text is not set
            message = f"{func.__name__}()" if not msg_text else msg_text
            logger.debug(
                QuesterTimer(
                    msg_type=msg_type,
                    message=message,
                    module=f"{func.__module__}",
                    latency=latency,
                ).toJSON()
            )
            return value

        return wrapper_analytics

    if func is None:
        # called with args - Return a decorator function that can read and return a function.
        return sub_decorator_analytics
    else:
        # called without arguments. Apply the decorator to the function immediately.
        return sub_decorator_analytics(func)


# TODO: Club async and sync analytics decorators
def async_analytics_decorator(
    func=None, *, msg_type: str = "timer", msg_text: str = ""
):
    """
    adds the json loggging to be caputured by kibana for analytics
    """

    def sub_decorator_analytics(func):
        ##  when a decorator uses arguments, you need to add an extra outer function.
        @wraps(func)
        async def wrapper_analytics(*args, **kwargs):
            start_time = time.perf_counter()
            value = await func(*args, **kwargs)
            end_time = time.perf_counter()
            latency: float = round(end_time - start_time, 6)
            # default to function name if msg_text is not set
            message = f"{func.__name__}()" if not msg_text else msg_text
            logger.debug(
                QuesterTimer(
                    msg_type=msg_type,
                    message=message,
                    module=f"{func.__module__}",
                    latency=latency,
                ).toJSON()
            )
            return value

        return wrapper_analytics

    if func is None:
        # called with args - Return a decorator function that can read and return a function.
        return sub_decorator_analytics
    else:
        # called without arguments. Apply the decorator to the function immediately.
        return sub_decorator_analytics(func)


# def timing_decorator(func):
#     async def process(func, *args, **kwargs):
#         if asyncio.iscoroutinefunction(func):
#             print("this function is a coroutine: {}".format(func.__name__))
#             return await func(*args, **kwargs)
#         else:
#             print("this is not a coroutine")
#             return func(*args, **kwargs)

#     async def helper(*args, **params):
#         print("{}.time".format(func.__name__))
#         start = time.perf_counter()
#         result = await process(func, *args, **params)

#         # Test normal function route...
#         # result = await process(lambda *a, **p: print(*a, **p), *args, **params)

#         print(">>>",time.perf_counter() - start)
#         return result

#     return helper


# class SyncAsyncDecoratorFactory:
#     @contextmanager
#     def wrapper(self, func, *args, **kwargs):
#         yield

#     def __call__(self, func):
#         @wraps(func)
#         def sync_wrapper(*args, **kwargs):
#             with self.wrapper(func, *args, **kwargs):
#                 return func(*args, **kwargs)

#         @wraps(func)
#         async def async_wrapper(*args, **kwargs):
#             with self.wrapper(func, *args, **kwargs):
#                 return await func(*args, **kwargs)

#         if asyncio.iscoroutinefunction(func):
#             return async_wrapper
#         else:
#             return sync_wrapper
