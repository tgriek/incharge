"""API for VattenFall InCharge integration."""

from http import HTTPStatus

import requests
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

    def authenticate(self):
        """Auth and retrieve JWT token."""
        try:
            headers = {**API_AUTH_SUB_KEY_HEADER, **API_REFERER_HEADER}
            response = requests.post(
                timeout=10000,
                url=API_BASE_URL + API_AUTH_PATH,
                headers=headers,
                auth=HTTPBasicAuth(self.username, self.password),
            )
            self.jwt_token = response.headers.get("Authorization")
            return response
        except requests.exceptions.HTTPError as incharge_connection_error:
            if (
                incharge_connection_error.response.status_code
                == HTTPStatus.UNAUTHORIZED
            ):
                raise  AuthorizationError from incharge_connection_error
            raise ConnectionError from incharge_connection_error

    def get_stations(self):
        """Get list of charging stations."""
        self.authenticate()
        try:
            headers = {
                "Authorization": self.jwt_token,
                **API_ENDPOINT_SUB_KEY_HEADER,
                **API_REFERER_HEADER,
            }
            response = requests.get(
                timeout=10000, url=API_BASE_URL + API_GET_STATIONS_PATH, headers=headers
            )
            result = [station["name"] for station in response.json()["stations"]]
            return result
        except requests.exceptions.HTTPError as incharge_connection_error:
            if (
                incharge_connection_error.response.status_code
                == HTTPStatus.UNAUTHORIZED
            ):
                raise AuthorizationError from incharge_connection_error
            raise ConnectionError from incharge_connection_error

    def get_station_consumption(
        self, station_id: str, since_date: str = "2000-01-01T00%3A00%3A00.00Z"
    ):
        """Get data for one charging station."""
        self.authenticate()
        try:
            headers = {
                "Authorization": self.jwt_token,
                **API_ENDPOINT_SUB_KEY_HEADER,
                **API_REFERER_HEADER,
                **API_ACCEPT_HEADER,
            }

            response = requests.get(
                timeout=10000,
                url=f"{API_BASE_URL}{API_GET_STATION_CONSUMPTION_PATH}{station_id}?since={since_date}",
                headers=headers,
            )
            return response.json()
        except requests.exceptions.HTTPError as incharge_connection_error:
            if (
                incharge_connection_error.response.status_code
                == HTTPStatus.UNAUTHORIZED
            ):
                raise AuthorizationError from incharge_connection_error
            raise ConnectionError from incharge_connection_error
