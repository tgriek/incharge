import json

test_response_stations = json.loads(
    json.dumps(
        {
            "stations": [
                {
                    "name": "station1",
                },
                {
                    "name": "station2",
                },
            ]
        }
    )
)

test_response_station_data = json.loads(json.dumps([{"total": 1000.00}]))

authorisation_response = json.loads(json.dumps({"Authorization": 'jwt_token'}))

authorisation_response_auth_endpoint_unauthorised = json.loads(
    json.dumps(
        {
            "timestamp": "2023-02-20T09:41:55",
            "message": "Login failed - incorrect username, password or configuration",
        }
    )
)

authorisation_response_endpoints_unauthorised = json.loads(
    json.dumps(
        {
            "timestamp": "2023-02-20T09:40:21.006+00:00",
            "status": 401,
            "error": "Unauthorized",
            "path": "/pub/consumption/",
        }
    )
)