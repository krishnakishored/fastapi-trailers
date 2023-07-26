import asyncio
from typing import List

import aiohttp

from clients.aiohttp_session import SingletonAiohttp
from common.logger import get_logger

logger = get_logger(__name__)


class AioHttpPostData:
    """The object of this class is used for making the async http request"""

    def __init__(
        self, url, payload, headers, auth_user=None, auth_pass=None
    ) -> None:
        self.url = url
        # stick to json payload for now
        self.payload = payload
        self.headers = headers
        self.auth_user = auth_user
        self.auth_pass = auth_pass


class AioHttpGetData:
    """The object of this class is used for making the async http request"""

    def __init__(
        self, url, params=None, headers=None, auth_user=None, auth_pass=None
    ) -> None:
        self.url = url
        # stick to json payload for now
        self.params = params
        self.headers = headers
        self.auth_user = auth_user
        self.auth_pass = auth_pass


class MakeAioHttpRequest:
    """subroutines that generate the http results using aiohttp
    All the other HTTP verbs shall have dedicated handlers if needed
    """

    @staticmethod
    async def post(req_obj: AioHttpPostData):
        # async with aiohttp.ClientSession() as session:
        try:
            result = b"{}"
            session = SingletonAiohttp.get_aiohttp_client()
            basic_auth = None
            if req_obj.auth_user is not None and req_obj.auth_pass is not None:
                # create an object of BasicAuth
                basic_auth = aiohttp.BasicAuth(
                    req_obj.auth_user, req_obj.auth_pass
                )

            async with session.post(
                req_obj.url,
                data=req_obj.payload,
                headers=req_obj.headers,
                auth=basic_auth,
            ) as resp:
                result = await resp.read()
        except asyncio.exceptions.TimeoutError as err:
            logger.warning(
                f"timeout - url:{req_obj.url}, params:{req_obj.params}"
            )
        finally:
            return result

    @staticmethod
    async def get(req_obj: AioHttpGetData):
        # async with aiohttp.ClientSession() as session:
        try:
            result = b"{}"
            session = SingletonAiohttp.get_aiohttp_client()
            basic_auth = None
            if req_obj.auth_user is not None and req_obj.auth_pass is not None:
                # create an object of BasicAuth
                basic_auth = aiohttp.BasicAuth(
                    req_obj.auth_user, req_obj.auth_pass
                )

            async with session.get(
                req_obj.url,
                params=req_obj.params,
                headers=req_obj.headers,
                auth=basic_auth,
            ) as resp:
                result = await resp.read()

        except asyncio.exceptions.TimeoutError as err:
            logger.warning(
                f"timeout - url:{req_obj.url}, params:{req_obj.params}"
            )
        finally:
            return result


class ProcessAioHttpTask:
    """
    Each of the methods(HTTP verbs)
    1. creates a task list from subroutines
    2. waits for them to finish via async.gather()
    added only POST, GET;
    all the other verbs shall have dedicated handlers if needed
    """

    @staticmethod
    async def post(req_obj_list: List[AioHttpPostData]):
        tasks = []
        result_collection = []
        try:
            for req_obj in req_obj_list:
                tasks.append(
                    asyncio.create_task(MakeAioHttpRequest.post(req_obj))
                )
            result_collection = await asyncio.gather(*tasks)
        except Exception as err:
            logger.exception(err)
        finally:
            return result_collection

    @staticmethod
    async def get(req_obj_list: List[AioHttpGetData]):
        tasks = []
        result_collection = []
        try:
            for req_obj in req_obj_list:
                tasks.append(
                    asyncio.create_task(MakeAioHttpRequest.get(req_obj))
                )
            result_collection = await asyncio.gather(*tasks)
        except Exception as err:
            logger.exception(err)
        finally:
            return result_collection


async def fetch_aiohttp_results(verb="GET", req_obj_list=[]):
    """
    does a conditional check based on HTTP verb
    and invokes the appropriate the ProcessAioHttpTask method
    """
    result = []
    # pdb.set_trace()
    try:
        if verb == "POST":
            result = await ProcessAioHttpTask.post(req_obj_list)
        elif verb == "GET":
            result = await ProcessAioHttpTask.get(req_obj_list)
    # except asyncio.TimeoutError
    except Exception as error:
        logger.exception(str(error))
        # TODO: handle it here?
    finally:
        return result
