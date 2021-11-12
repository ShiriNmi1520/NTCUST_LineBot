from os import path, remove
import firebase_admin
from firebase_admin import credentials, db
from google.cloud import secretmanager
from google.oauth2 import service_account
import json
from datetime import datetime

# Get firebase access key from gcp secret manager
credentials = service_account.Credentials.from_service_account_file(
    path.relpath("pk/secret_manager.json"))
client = secretmanager.SecretManagerServiceClient(credentials=credentials)
name = f""

response = client.access_secret_version(request={"name": name})

payload = response.payload.data.decode("UTF-8")

# temp save payload to json file for firebase init
with open(path.relpath("pk/firebase_pk.json"), "w") as file:
  file.write(payload)


# Init firebase
fb_cred = firebase_admin.credentials.Certificate(
    path.relpath("pk/firebase_pk.json"))
fb_app = firebase_admin.initialize_app(
    fb_cred, {"databaseURL": ""})

# remove temp firebase pk file
try:
  remove(path.relpath("pk/firebase_pk.json"))
except OSError:
  pass


def writeToFireBase(type, data):
  ref = db.reference('{0}/'.format(type))
  ref.push(data)


def addSchedule(uid, data):
  ref = db.reference("schedule/{0}".format(uid))
  ref.push(data)


def getSchedule(uid):
  ref = db.reference("schedule/{0}".format(uid))
  return ref.get()


def addAccounting(uid, category, yearMonth, data):
  ref = db.reference("accounting/{0}/{1}/{2}".format(uid, category, yearMonth))
  ref.push(data)


def taskSchedule():
  now = datetime.now()
  data = dict()

  ids = db.reference('schedule/').get()
  for key in list(ids.keys()):
    dataArray = []
    schedule = db.reference('schedule').child('{0}'.format(key)).get()

    for key1, value in schedule.items():
      if(value['date'] == datetime.today().strftime('%Y/%m/%d') and value['time'] == '{0}:{1}'.format(now.hour, now.minute)):
        dataArray.append(value)
        data[key] = dataArray
  return data


def updateLocation(uid, data):
  ref = db.reference("location/{0}".format(uid))
  ref.update(data)


def getLocation(uid):
  ref = db.reference("location/{0}".format(uid))
  return ref.get()


def addBusRoute(busNo, direction, data):
  ref = db.reference("busRoute/{0}/{1}".format(direction, busNo))
  ref.push(data)


def addBusStops(stop, direction, busNo):
  ref = db.reference("busStop/{0}/{1}".format(stop, direction))
  ref.push(busNo)


def getByPassBus(stop):
  ref_outbound = db.reference("busStop/{0}/0".format(stop))
  ref_inbound = db.reference("busStop/{0}/1".format(stop))

  data_outbound = ref_outbound.get()
  data_inbound = ref_inbound.get()
  data = []
  for item in data_outbound.keys():
    data.append(data_outbound[item]["busNo"])

  for item in data_inbound.keys():
    data.append(data_inbound[item]["busNo"])

  
  return data


if __name__ == "__main__":
  # print(getLocation("Ub1843b600491fba7f9bc511f960a6c67"))
  print(getByPassBus("朝陽科技大學"))
