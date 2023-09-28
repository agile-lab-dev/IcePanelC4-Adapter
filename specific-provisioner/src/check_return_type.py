import inspect
import json
from typing import Any

from fastapi import FastAPI
from fastapi.routing import APIRoute
from pydantic import BaseModel
from starlette.responses import Response

from src.app_config import app
from src.models.api_models import SystemErr
from src.utility.logger import get_logger

logger = get_logger()


def check_response(
    out_response: Any,
    responses: dict | None = None,
    route_path: str | None = None,
    application: FastAPI = app,
) -> Response:
    """
    Check if the type of out_response is included in one of:
    - the responses param
    - in the responses of the specified route
    - in the responses of the caller route

    and, in case, returns a Response object that includes the HTTP response code and
    the JSON or the text corresponding to the out_response parameter.
    If the type is not accepted it returns a Response containing a SystemErr.

    Args:
        out_response: (Any) The response that the FastAPI route wants to return as output.
        responses: (dict, optional) A dictionary used to specify the possible responses for the route.
            It is used to define the possible HTTP response codes that the API can return along with their details,
            including the data model to be returned. Defaults to None.
        route_path: (str, optional) The path of the FastAPI route. Defaults to None.
        application: (FastAPI, optional) The FastAPI application. Defaults to the main application.

    Returns:
        starlette.responses.Response: A Response object that includes the HTTP response code and
        the JSON or the text corresponding to the out_response parameter.
    """  # noqa: E501

    if responses is not None:
        return _check_response_type(responses, out_response)

    if route_path is not None:
        endpoint = _find_caller_endpoint_by_path(
            application=application, caller_path=route_path
        )

    else:
        caller_function = _find_caller_function()

        if caller_function is None:
            logger.error("Check_responses: caller function not found")
            return Response(
                status_code=500,
                content=SystemErr(
                    error="An unexpected error occurred while processing the request. "
                    "If the issue still persists, contact the platform team for assistance!"  # noqa: E501
                ).model_dump_json(),
                media_type="application/json",
            )

        endpoint = _find_caller_endpoint_by_name(
            application=application, caller_name=caller_function
        )

    responses = endpoint.responses if endpoint is not None else None

    if responses is None:
        logger.error(
            "Check_responses: endpoint not found in app.routes or responses parameter has no value "  # noqa: E501
        )
        return Response(
            status_code=500,
            content=SystemErr(
                error="An unexpected error occurred while processing the request. "
                "If the issue still persists, contact the platform team for assistance!"  # noqa: E501
            ).model_dump_json(),
            media_type="application/json",
        )

    return _check_response_type(responses, out_response)


def _check_response_type(responses: dict, out_response: Any) -> Response:
    """
    Ensures that the type of the parameter 'out_response' is contained in the 'model'
    field of the 'responses' dictionary.

    Args:
        responses: (dict) A dictionary used to specify the possible responses for the route.
            It is used to define the possible HTTP response codes that the API can return along with their details,
            including the data model to be returned.
        out_response: (Any) The response that the FastAPI route wants to return as output.
    Returns:
        starlette.responses.Response: A Response object that includes the HTTP response code and
        the JSON or the text corresponding to the out_response parameter.
        If the type of 'out_response' is not accepted as per the 'model' field in 'responses',
        it returns a Response containing a SystemErr.
    """  # noqa: E501

    # set default response_code = 500, if correct response type is found it will be changed  # noqa: E501
    response_code = 500
    correct_output_type = False
    for k in responses.keys():
        endpoint_response = responses.get(k)
        if isinstance(endpoint_response, dict) and endpoint_response is not None:
            if endpoint_response.get("model") == type(out_response):
                correct_output_type = True
                response_code = k
                break

    if not correct_output_type:
        logger.error("Check response type: response type indicated not allowed")
        return Response(
            status_code=500,
            content=SystemErr(
                error="An unexpected error occurred while processing the request. "
                "If the issue still persists, contact the platform team for assistance!"  # noqa: E501
            ).model_dump_json(),
            media_type="application/json",
        )

    if isinstance(out_response, BaseModel):
        content = json.dumps(out_response.model_dump())
        media_type = "application/json"
    elif isinstance(out_response, list) and all(
        isinstance(item, BaseModel) for item in out_response
    ):  # noqa: E501
        out_response_dicts = [item.dict() for item in out_response]
        content = json.dumps(out_response_dicts)
        media_type = "application/json"
    else:
        content = str(out_response)
        media_type = "text/plain"

    return Response(
        status_code=int(response_code), content=content, media_type=media_type
    )


def _find_caller_function(n_back: int = 2) -> str | None:
    """
    Returns the name of the caller function 'n_back' frames up the call stack.

    This function inspects the call stack to find the name of the caller function
    'n_back' frames up from the current function call. If 'n_back' is not specified,
    it defaults to 2.

    Args:
        n_back (int, optional): The number of frames up the call stack to look for
            the caller function. Defaults to 2, which retrieves the immediate caller.

    Returns:
        str | None: The name of the caller function as a string, or None if the caller
        function cannot be determined (e.g., when 'n_back' exceeds the call stack depth
        or when this function is executed at the highest level in the call stack).
    """  # noqa: E501

    frame = inspect.currentframe()

    if frame is not None:
        for _ in range(n_back):
            if frame is None:
                return None
            frame = frame.f_back

    caller_function = frame.f_code.co_name if frame is not None else None
    return caller_function


def _find_caller_endpoint_by_path(
    application: FastAPI, caller_path: str
) -> APIRoute | None:
    """
    Find and return the FastAPI endpoint (APIRoute) based on the provided caller_path.

    This function iterates through all registered routes in the FastAPI application and searches for an APIRoute
    that matches the caller_path argument.
    If a match is found, the corresponding APIRoute object is returned. If no match is found, the function returns None.

    Args:
        application (FastAPI): The FastAPI application instance to search for the endpoint.
        caller_path (str): The path of the route to search for.

    Returns:
        APIRoute or None: If a matching route is found, it returns the corresponding APIRoute object.
        If no matching route is found, it returns None.

    """  # noqa: E501

    for route in application.routes:
        if isinstance(route, APIRoute) and route.path == caller_path:
            return route

    return None


def _find_caller_endpoint_by_name(
    application: FastAPI, caller_name: str
) -> APIRoute | None:
    """
    Find and return the FastAPI endpoint (APIRoute) based on the provided caller_name.

    This function iterates through all registered routes in the FastAPI application and searches for an APIRoute
    that matches the caller_name argument.
    If a match is found, the corresponding APIRoute object is returned. If no match is found, the function returns None.

    Args:
        application (FastAPI): The FastAPI application instance to search for the endpoint.
        caller_name (str): The name of the route to search for.

    Returns:
        APIRoute or None: If a matching route is found, it returns the corresponding APIRoute object.
        If no matching route is found, it returns None.

    """  # noqa: E501

    for route in application.routes:
        if isinstance(route, APIRoute) and route.name == caller_name:
            return route

    return None
