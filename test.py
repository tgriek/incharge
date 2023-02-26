from incharge.api import InCharge

api = InCharge("tim.van.grieken", "msYhLmL!FWFWx2J")

#Get a list of stations
stations = api.get_stations().json()
print(stations)

#Get total consumption data for one station 
data = api.get_station_consumption('ALF-0012036').json()
print(data[0]['total'])
