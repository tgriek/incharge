import requests_mock
import json
import pytest

from http import HTTPStatus
from incharge.api import InCharge
from . import (
    authorisation_response,
    authorisation_response_auth_endpoint_unauthorised,
    test_response_station_data,
    test_response_stations
)
from incharge.exceptions import AuthorizationError

def test_auth_authorized():
    with requests_mock.Mocker() as mock_request:
        mock_request.post(
            "https://businessspecificapimanglobal.azure-api.net/old-authorization/incharge-api/user/token",
            headers=authorisation_response,
            status_code=HTTPStatus.OK
        )
        api = InCharge('someuser', 'somepassword')
        response = api.authenticate()
        assert response.status_code == HTTPStatus.OK
        assert len(response.content) == 0


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
      


def test_get_stations():
     with requests_mock.Mocker() as mock_request:
        mock_request.post(
            "https://businessspecificapimanglobal.azure-api.net/old-authorization/incharge-api/user/token",
            headers=authorisation_response,
            status_code=HTTPStatus.OK
        )
        mock_request.get(
            "https://businessspecificapimanglobal.azure-api.net/station-configuration/pub/stations",
            json=test_response_stations,
            status_code=HTTPStatus.OK,
        )
        api = InCharge('someuser', 'somepassword')
        response = api.get_stations()
        assert response.status_code == HTTPStatus.OK
        assert response.json()['stations'][0]['name'] == 'station1'

def test_get_stations_unauthorized():
     with requests_mock.Mocker() as mock_request:
        mock_request.post(
            "https://businessspecificapimanglobal.azure-api.net/old-authorization/incharge-api/user/token",
            json=authorisation_response_auth_endpoint_unauthorised,
            status_code=HTTPStatus.UNAUTHORIZED
        )
        api = InCharge('someuser', 'somepassword')
        response = api.get_stations()
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        
def test_get_station_consumption():
    with requests_mock.Mocker() as mock_request:
        mock_request.post(
            "https://businessspecificapimanglobal.azure-api.net/old-authorization/incharge-api/user/token",
            headers=authorisation_response,
            status_code=HTTPStatus.OK
        )
        ## Get stations
        mock_request.get(
            "https://businessspecificapimanglobal.azure-api.net/station-configuration/pub/stations",
            json=test_response_stations,
            status_code=HTTPStatus.OK,
        )
        ## Get data for one station
        mock_request.get(
            "https://businessspecificapimanglobal.azure-api.net/energy-consumptions/pub/consumption/station1?since=2000-01-01T00%3A00%3A00.00Z",
            json=test_response_station_data,
            status_code=HTTPStatus.OK,
        )
        api = InCharge('someuser', 'somepassword')
        response = api.get_station_consumption(station_name='station1')
        
        assert response.status_code == HTTPStatus.OK
        assert response.json()[0]['total'] == 1000.00

def test_get_station_consumption_unauthorized():
    with requests_mock.Mocker() as mock_request:
        mock_request.post(
            "https://businessspecificapimanglobal.azure-api.net/old-authorization/incharge-api/user/token",
            json=authorisation_response_auth_endpoint_unauthorised,
            status_code=HTTPStatus.UNAUTHORIZED
        )
        api = InCharge('someuser', 'somepassword')
        response = api.get_station_consumption(station_name='station1')
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        
