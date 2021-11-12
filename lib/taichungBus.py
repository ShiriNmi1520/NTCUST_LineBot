from requests import request, Request
import requests
from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from firebase import addBusStops, getByPassBus
import base64


class Auth():
  def __init__(self, app_id, app_key):
    self.app_id = app_id
    self.app_key = app_key

  def get_auth_header(self):
    xdate = format_date_time(mktime(datetime.now().timetuple()))
    hashed = hmac.new(self.app_key.encode("utf8"),
                      ("x-date: " + xdate).encode("utf8"), sha1)
    signature = base64.b64encode(hashed.digest()).decode()

    authorization = 'hmac username="' + self.app_id + '", ' + \
        'algorithm="hmac-sha1", ' + \
        'headers="x-date", ' + \
        'signature="' + signature + '"'

    return {
        'Authorization': authorization,
        'x-date': format_date_time(mktime(datetime.now().timetuple())),
        'Accept - Encoding': 'gzip'
    }


def getNearbyStation(data):
  result = dict()
  tempData = []
  location = str(data["latitude"]) + ',' + str(data["longitude"])
  payload = dict(location=location, radius=500, type="transit_station",
                 language="zh-TW", key="AIzaSyAinoByFiwvTTi_4knnEomhu_YfK0N0oZs")
  request = requests.get(
      "https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=payload)
  for index in request.json()["results"]:
    tempData.append(index["name"])

  tempData = list(set(tempData))

  for item in tempData:
    result[item] = getByPassBus(item)
    result[item] = list(dict.fromkeys(result[item]))

  print(result)
  return result


def getDetailedBus(busNo, data):
  a = Auth("", "")
  result = dict()
  tempData = []
  location = str(data["latitude"]) + ',' + str(data["longitude"])
  payload = dict(location=location, radius=500, type="transit_station",
                 language="zh-TW", key="AIzaSyAinoByFiwvTTi_4knnEomhu_YfK0N0oZs")
  request = requests.get(
      "https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=payload)
  for index in request.json()["results"]:
    tempData.append(index["name"])

  tempData = list(set(tempData))
  temp = dict()
  temp["0"] = dict()
  temp["1"] = dict()
  for item in tempData:
    request_url = "https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/City/Taichung/{0}".format(
        busNo)
    payload = dict()
    payload["$select"] = "PlateNumb,StopName,Direction,NextBusTime,StopStatus"
    payload["$filter"] = "Direction eq '0' and StopName/Zh_tw eq '{0}'".format(item)
    payload["$orderby"] = "EstimateTime"
    response = requests.get(
        request_url, headers=a.get_auth_header(), params=payload)
    data = response.json()
    result[item] = []
    for item1 in data:
      if "StopStatus" in item1:
        if item1["StopStatus"] != 3 and "EstimateTime" in item1.keys():
          temp["0"]["PlateNumb"] = item1["PlateNumb"]
          temp["0"]["EstimateTime"] = item1["EstimateTime"]
          result[item].append(temp.copy())
        elif item1["StopStatus"] == 3:
          temp["0"]["PlateNumb"] = ""
          temp["0"]["EstimateTime"] = None
          temp["0"]["Message"] = "末班車駛離"
        elif item1["StopStatus"] == 2:
          temp["0"]["PlateNumb"] = ""
          temp["0"]["EstimateTime"] = None
          temp["0"]["Message"] = "交管不停"
        else:
          temp["0"]["PlateNumb"] = ""
          temp["0"]["EstimateTime"] = None
          temp["0"]["Message"] = "無法取得該站點資訊"

  for item in tempData:
    request_url = "https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/City/Taichung/{0}".format(
        busNo)
    payload = dict()
    payload["$select"] = "PlateNumb,StopName,Direction,NextBusTime,StopStatus"
    payload["$filter"] = "Direction eq '1' and StopName/Zh_tw eq '{0}'".format(item)
    payload["$orderby"] = "EstimateTime"
    response = requests.get(
        request_url, headers=a.get_auth_header(), params=payload)
    data = response.json()
    result[item] = []
    for item1 in data:
      if "StopStatus" in item1:
        if item1["StopStatus"] != 3 and "EstimateTime" in item1.keys():
          temp["0"]["PlateNumb"] = item1["PlateNumb"]
          temp["0"]["EstimateTime"] = item1["EstimateTime"]
          result[item].append(temp.copy())
        elif item1["StopStatus"] == 3:
          temp["0"]["PlateNumb"] = ""
          temp["0"]["EstimateTime"] = None
          temp["0"]["Message"] = "末班車駛離"
        elif item1["StopStatus"] == 2:
          temp["0"]["PlateNumb"] = ""
          temp["0"]["EstimateTime"] = None
          temp["0"]["Message"] = "交管不停"
        else:
          temp["0"]["PlateNumb"] = ""
          temp["0"]["EstimateTime"] = None
          temp["0"]["Message"] = "無法取得該站點資訊"

  return result


def directionRoute(departure, destination):
  try:
    location = str(departure["latitude"]) + ',' + str(departure["longitude"])
    payload = dict(language="zh-TW", origin=location, destination=destination,
                   mode="transit", key="AIzaSyAinoByFiwvTTi_4knnEomhu_YfK0N0oZs")
    request = requests.get(
        "https://maps.googleapis.com/maps/api/directions/json", params=payload)
    data = dict()
    data["estimatedTimeArrival"] = request.json(
    )["routes"][0]["legs"][0]["arrival_time"]["text"]
    data["estimatedTimeDeparture"] = request.json(
    )["routes"][0]["legs"][0]["departure_time"]["text"]
    data["routeDistance"] = request.json(
    )["routes"][0]["legs"][0]["distance"]["text"]
    data["departureAddress"] = request.json(
    )["routes"][0]["legs"][0]["start_address"]
    data["arrivalAddress"] = request.json(
    )["routes"][0]["legs"][0]["end_address"]
    data["walkTime"] = request.json(
    )["routes"][0]["legs"][0]["steps"][0]["duration"]["text"]
    data["duration"] = request.json()["routes"][0]["legs"][0]["duration"]["text"]
    data["bus"] = []
    busRoute = list(filter(lambda route: route["travel_mode"] == "TRANSIT", request.json()[
        "routes"][0]["legs"][0]["steps"]))
    for item in busRoute:
      busInfo = dict()
      busInfo["distance"] = item["distance"]["text"]
      busInfo["duration"] = item["duration"]["text"]
      busInfo["arrivalStop"] = item["transit_details"]["arrival_stop"]["name"]
      busInfo["arrivalTime"] = item["transit_details"]["arrival_time"]["text"]
      busInfo["departureStop"] = item["transit_details"]["departure_stop"]["name"]
      busInfo["departureTime"] = item["transit_details"]["departure_time"]["text"]
      busInfo["busNo"] = item["transit_details"]["line"]["short_name"]
      busInfo["stops"] = item["transit_details"]["num_stops"]
      data["bus"].append(busInfo)

    return data
  except:
    return None


def getBusRoute(skip, count):
  params = dict(top=count if count else 30,
                skip=skip if skip else 0,
                format="JSON",)
  a = Auth("", "")
  response = request('get', 'https://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/City/Taichung',
                     headers=a.get_auth_header(), params=params)
  data = response.json()
  result = dict()
  for item in data:
    ##print(ic, item["Direction"])
    route = []

    for stop in item["Stops"]:
      # route.append(stop["StopName"]["Zh_tw"])
      addBusStops(stop["StopName"]["Zh_tw"], item["Direction"], {
                  "busNo": item["SubRouteName"]["Zh_tw"]})
