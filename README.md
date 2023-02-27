# Vattenfall InCharge
Python implemenation of the Vattenfall InCharge API

## Usage

```python
from incharge.api import InCharge

api = InCharge(<username>, <password>)

#Get a list of stations
stations = api.get_stations().json()
print(stations)

#Get total consumption data for one station 
data = api.get_station_consumption(<station_name>).json()
print(data[0]['total'])
```
## Description
This package currently supports

`api.get_stations()` Get list of stations.

`api.get_station_consumption(station_name, since_date)` Get consumption of a single station based on its name.
