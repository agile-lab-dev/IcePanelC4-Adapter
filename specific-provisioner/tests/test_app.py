import json
import unittest

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response
from starlette.testclient import TestClient

from src.check_return_type import check_response
from src.models.api_models import SystemErr, ValidationError

app2 = FastAPI()


class RequestModel(BaseModel):
    val: int


@app2.post(
    "/v1/test",
    response_model=None,
    responses={
        "200": {"model": int},
        "202": {"model": str},
        "500": {"model": SystemErr},
    },
)
def fun1(request: RequestModel) -> Response:
    if request is not None:
        val = request.val

    if val == 1:
        return check_response(out_response=1, application=app2)

    if val == 2:
        return check_response(out_response="ris=202", application=app2)

    if val == 3:
        resp = SystemErr(error="error")
        return check_response(out_response=resp, application=app2)

    else:
        resp2 = ValidationError(errors=["wrong input"])
        return check_response(out_response=resp2, application=app2)


client = TestClient(app2)


class testApp(unittest.TestCase):
    def test_fun1_valid_input_200(self):
        import pydantic

        print(pydantic.__file__)
        print(pydantic.__version__)

        response = client.post("/v1/test", json={"val": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "1")

    def test_fun1_valid_input_202(self):
        response = client.post("/v1/test", json={"val": 2})
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.text, "ris=202")

    def test_fun1_valid_input_500(self):
        response = client.post("/v1/test", json={"val": 3})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "error"})

    def test_fun1_invalid_input_500(self):
        response = client.post("/v1/test", json={"val": 4})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json(),
            {
                "error": "An unexpected error occurred while processing the request. "
                "If the issue still persists, contact the platform team for assistance!"
            },
        )  # noqa: E501

    def test_fun1_missing_input_422(self):
        response = client.post("/v1/test")
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.json())


class TestCheckResponses(unittest.TestCase):
    def test_check_responses_valid_response(self):
        # Test a valid response for status code 200
        out_response = 1
        responses = {"200": {"model": int}}
        response = check_response(
            application=app2, out_response=out_response, responses=responses
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.body), 1)

    def test_check_responses_invalid_response(self):
        out_response = 1
        responses = None
        response = check_response(
            application=app2, out_response=out_response, responses=responses
        )
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", json.loads(response.body))

    def test_check_responses_invalid_response2(self):
        out_response = "ciao"
        responses = {"200": {"model": int}}
        response = check_response(
            application=app2, out_response=out_response, responses=responses
        )
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", json.loads(response.body))
