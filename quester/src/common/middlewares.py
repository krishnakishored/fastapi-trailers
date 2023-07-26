import json
import time

from fastapi import Request
from starlette.background import BackgroundTask

from common.analytics import QuesterAnalyticsRequest, QuesterAnalyticsResponse
from common.logger import get_logger

logger = get_logger(__name__, log_type="json")


async def write_response_log(
    request: Request, response, transaction_id: str, process_time: float
):
    # don't log requests & responses to this list of apis:
    logging_discarded_apis = ["/status"]
    # only status_code is enough,response_body is not logged
    # obj_resp["level"] = logger.getEffectiveLevel()
    # if request.url.path in logging_request_body:
    #     body = await request.json()
    #     logger.info(body)

    if request.url.path not in logging_discarded_apis:
        obj_resp = QuesterAnalyticsResponse(
            msg_type="response",
            transaction_id=transaction_id,
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            latency=process_time,
        ).__dict__
        logger.info(json.dumps(obj_resp))


async def request_response_logger(request: Request, call_next):
    """middleware to log resquest & response status_code as info"""
    import uuid

    ##TODO  verify X-Transaction-ID from header instead
    if "X-Transaction-ID" in request.headers.keys():
        transaction_id = request.headers["X-Transaction-ID"]
    elif "x-transaction-id" in request.headers.keys():
        transaction_id = request.headers["x-transaction-id"]
    else:
        transaction_id = str(uuid.uuid4())

    # don't log requests & responses to this list of apis:
    logging_discarded_apis = ["/status"]

    if request.url.path not in logging_discarded_apis:
        query_parameters = {}
        if request.query_params:
            # Don't log api_key
            query_parameters = {
                key: val
                for key, val in request.query_params.items()
                if key != "api_key"
            }
        obj_req = QuesterAnalyticsRequest(
            msg_type="request",
            transaction_id=transaction_id,
            method=request.method,
            path=request.url.path,
            api_key=request.query_params.get("api_key", "NOAPIKEY"),
            query_params=query_parameters,
        ).__dict__
        logger.info(json.dumps(obj_req))

        # logging_request_body = ["/componentGeocode", "/componentReverseGeocode"]
        # if request.url.path in logging_request_body:
        #     body = await request.json()
        #     logger.info(body)
    start_time = time.perf_counter()
    # response is of type starlette.responses.StreamingResponse
    response = await call_next(request)
    process_time = round(time.perf_counter() - start_time, 6)
    # starlette's background task should be attached to a response, and will run only once the response has been sent.
    response.background = BackgroundTask(
        write_response_log, request, response, transaction_id, process_time
    )
    return response


## TODO: temporary fix : adding two middlewares causes 502- Bad gateway errors.
## So grouped the two middlewares into one
async def add_security_headers_log_req_res(request: Request, call_next):
    """Adds security headers and logs requests and responses

    Args:
        request (Request): _description_
        call_next (_type_): _description_

    Returns:
        _type_: _description_
    """
    import uuid

    ##TODO  verify X-Transaction-ID from header instead
    if "X-Transaction-ID" in request.headers.keys():
        transaction_id = request.headers["X-Transaction-ID"]
    elif "x-transaction-id" in request.headers.keys():
        transaction_id = request.headers["x-transaction-id"]
    else:
        transaction_id = str(uuid.uuid4())

    # don't log requests & responses to this list of apis:
    logging_discarded_apis = ["/status"]

    if request.url.path not in logging_discarded_apis:
        query_parameters = {}
        if request.query_params:
            # Don't log api_key
            query_parameters = {
                key: val
                for key, val in request.query_params.items()
                if key != "api_key"
            }
        obj_req = QuesterAnalyticsRequest(
            msg_type="request",
            transaction_id=transaction_id,
            method=request.method,
            path=request.url.path,
            api_key=request.query_params.get("api_key", "NOAPIKEY"),
            query_params=query_parameters,
        ).__dict__
        logger.info(json.dumps(obj_req))
    start_time = time.perf_counter()
    # response is of type starlette.responses.StreamingResponse
    response = await call_next(request)

    response.headers["X-XSS-Protection"] = str(1)
    response.headers["X-Frame-Options"] = "Deny"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = "default-src 'none'"
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    response.headers["Access-Control-Allow-Origin"] = "*"

    process_time = round(time.perf_counter() - start_time, 6)
    # starlette's background task should be attached to a response, and will run only once the response has been sent.
    response.background = BackgroundTask(
        write_response_log, request, response, transaction_id, process_time
    )
    return response


async def add_security_headers(request: Request, call_next):
    """Add the heaaders to address vulnerability scan issues

    call_next() will pass the request to the corresponding path operation
    returns the response which can be modified before return it
    """

    response = await call_next(request)
    response.headers["X-XSS-Protection"] = str(1)
    response.headers["X-Frame-Options"] = "Deny"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = "default-src 'none'"
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


async def add_process_time_header(request: Request, call_next):
    """Sample middleware to add process-time as custom header

    Need not be used in production
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
