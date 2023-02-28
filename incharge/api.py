"""API for VattenFall InCharge integration."""

from http import HTTPStatus

import requests
import json

from requests import Response
from requests.auth import HTTPBasicAuth

from incharge.const import (
    API_ACCEPT_HEADER,
    API_AUTH_PATH,
    API_AUTH_SUB_KEY_HEADER,
    API_BASE_URL,
    API_ENDPOINT_SUB_KEY_HEADER,
    API_GET_STATION_CONSUMPTION_PATH,
    API_GET_STATIONS_PATH,
    API_REFERER_HEADER,
)
from incharge.exceptions import AuthorizationError


class InCharge:
    """Implementation of the InCharge API."""

    def __init__(self, username: str, password: str) -> None:
        """Init with username and password."""
        self.username = username
        self.password = password
        self.jwt_token = ""

    def authenticate(self) -> Response:
        """Auth and retrieve JWT token."""
        headers = {**API_AUTH_SUB_KEY_HEADER, **API_REFERER_HEADER}
        response = requests.post(
            timeout=10000,
            url=API_BASE_URL + API_AUTH_PATH,
            headers=headers,
            auth=HTTPBasicAuth(self.username, self.password),
        )
        self.jwt_token = response.headers.get("Authorization")
        return response
    

    def get_stations(self) -> Response:
        """Get list of charging stations."""
        self.authenticate()
        headers = {
            "Authorization": self.jwt_token,
            **API_ENDPOINT_SUB_KEY_HEADER,
            **API_REFERER_HEADER,
        }
        response = requests.get(
            timeout=10000, url=API_BASE_URL + API_GET_STATIONS_PATH, headers=headers
        )
        return response


    def get_station_consumption(
        self, station_name: str, since_date: str = "2000-01-01T00%3A00%3A00.00Z"
    ) -> Response:
        """Get consumption data for one charging station.""" 
        self.authenticate()
        headers = {
            "Authorization": self.jwt_token,
            **API_ENDPOINT_SUB_KEY_HEADER,
            **API_REFERER_HEADER,
            **API_ACCEPT_HEADER,
        }

        response = requests.get(
            timeout=10000,
            url=f"{API_BASE_URL}{API_GET_STATION_CONSUMPTION_PATH}{station_name}?since={since_date}",
            headers=headers,
        )
        return response
    