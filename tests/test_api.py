import requests_mock
import json

from http import HTTPStatus
from incharge.api import InCharge
from . import authorisation_response_auth_endpoint_unauthorised


def test_auth_unauthorized():
    with requests_mock.Mocker() as mock_request:
        mock_request.post(
            "https://businessspecificapimanglobal.azure-api.net/old-authorization/incharge-api/user/token",
            json=authorisation_response_auth_endpoint_unauthorised,
            status_code=HTTPStatus.UNAUTHORIZED
        )
        api = InCharge('someuser', 'somepassword')
        response = api.authenticate()
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert api.jwt_token is None