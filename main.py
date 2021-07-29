import json
import requests
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

def get_live_data():
    try:
        base_url = config["API"]["base_url"]
        result = requests.get(base_url+"live-data")
        return json.loads(result.text)
    except:
        print("Error: Live API could not be reached.")



def get_building_data(interval=60, begin_timestamp=1635869520, end_timestamp=1635894000):
    try:
        base_url = config["API"]["base_url"]
        result = requests.get(base_url+"building?interval="+str(interval)+"&begin-timestamp="+str(begin_timestamp)+"&end-timestamp="+str(end_timestamp))
        return json.loads(result.text)
    except:
        print("Error: Building API could not be reached.")


def get_room_data(interval=60, begin_timestamp=1635869520, end_timestamp=1635894000):
    try:
        base_url = config["API"]["base_url"]
        result = requests.get(base_url+"room?interval="+str(interval)+"&begin-timestamp="+str(begin_timestamp)+"&end-timestamp="+str(end_timestamp))
        return json.loads(result.text)
    except:
        print("Error: Room API could not be reached.")


def get_raspi_sensordata():
    try:
        url = config["RASPBERRY"]["url"]
        result = requests.get(url)
        return json.loads(result.text)
    except:
        print("Error: Raspberry Pi could not be reached.")


def get_currently_wasteful_rooms():
    rooms = []
    data = get_live_data()
    for room in data["rooms"]:
        if room["workplaceReservations"] == 0 and (room["sensors"]["airConditioningRunning"] or room["sensors"]["heaterRunning"]):
            rooms.append(room["id"])

    return rooms



print(get_currently_wasteful_rooms())
#print(get_raspi_sensordata())
#print(get_room_data())
#print(get_building_data())
#print(get_live_data())


