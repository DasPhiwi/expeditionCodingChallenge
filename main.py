import json
from datetime import datetime
from tqdm import tqdm

import requests
import configparser
import pandas as pd
import pdb
import model
import numpy as np

config = configparser.ConfigParser()
config.read("config.ini")


def get_live_data():
    try:
        base_url = config["API"]["base_url"]
        result = requests.get(base_url + "live-data")
        return json.loads(result.text)
    except:
        print("Error: Live API could not be reached.")


def get_building_data(interval=60, begin_timestamp=1635869520, end_timestamp=1635894000):
    try:
        base_url = config["API"]["base_url"]
        result = requests.get(base_url + "building?interval=" + str(interval) + "&begin-timestamp=" + str(
            begin_timestamp) + "&end-timestamp=" + str(end_timestamp))
        return json.loads(result.text)
    except:
        print("Error: Building API could not be reached.")


def get_room_data(interval=60, begin_timestamp=1635869520, end_timestamp=1635894000):
    try:
        base_url = config["API"]["base_url"]
        result = requests.get(base_url + "room?interval=" + str(interval) + "&begin-timestamp=" + str(
            begin_timestamp) + "&end-timestamp=" + str(end_timestamp))
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


def json_to_data():
    result_features = pd.DataFrame(columns=['lightOn', 'windowsOpen', 'rollerBlindsClosed', 'airConditioningRunning',
                                            'heaterRunning'])
    result_labels = pd.DataFrame(columns=['powerConsumption'])
    for i in tqdm(range(25)):
        for room_data in get_room_data(interval=120, begin_timestamp=1595887200 + i * 86400, end_timestamp=1595887200
                                                                                                           + (
                                                                                                                   i + 1) * 86400):
            for room in room_data["rooms"]:
                features = list(room["sensors"].keys())
                values = list(room["sensors"].values())
                features_df = pd.DataFrame([values], columns=features)
                result_features = result_features.append(features_df, ignore_index=True)
                labels_df = pd.DataFrame([room["powerConsumption"]], columns=["powerConsumption"])
                result_labels = result_labels.append(labels_df, ignore_index=True)
    result_features.to_csv("data.csv")
    result_labels.to_csv("labels.csv")


def check_powerConsumption_per_room():
    room_data = get_live_data()
    room_with_high_power = []
    for room in room_data["rooms"]:
        # features = list(room["sensors"].keys())
        values = list(room["sensors"].values())
        estimated_powerConsumption = float(model.prediction_(np.array(values).reshape(1, -1)))
        actual_powerConsumption = room["powerConsumption"]

        if actual_powerConsumption > estimated_powerConsumption * 1.2:
            room_with_high_power.append(
                {'id': room["id"], "difference": abs(actual_powerConsumption - estimated_powerConsumption)})

    return room_with_high_power


def get_room_status():
    raspi_data = get_raspi_sensordata()
    live_data = get_live_data()
    live_time = datetime.fromtimestamp(live_data['samplingStartTime']).strftime("%d.%m.%Y %H:%M:%S")
    high_powered_rooms = check_powerConsumption_per_room()
    rooms = []
    tvoc_outside = raspi_data["tvoc"]
    for room in live_data["rooms"]:
        messages = []
        if room["workplaceReservations"] == 0 and room["sensors"]["airConditioningRunning"]:
            messages.append("In diesem Raum sind keine Personen eingebucht, aber die Klimaanlage ist an.")
        if room["workplaceReservations"] == 0 and room["sensors"]["heaterRunning"]:
            messages.append("In diesem Raum sind keine Personen eingebucht, aber die Heizung ist an.")
        if room["sensors"]["airConditioningRunning"] and room["sensors"]["heaterRunning"]:
            messages.append("In diesem Raum sind sowohl Klimaanlage als auch Heizung an.")
        if room["sensors"]["windowsOpen"] and room["sensors"]["heaterRunning"]:
            messages.append("In diesem Raum sind sowohl Fenster offen als auch Heizung an.")
        if room["sensors"]["windowsOpen"] and room["sensors"]["heaterRunning"]:
            messages.append("In diesem Raum sind sowohl Klimaanlage als auch Heizung an.")
        if room["sensors"]["windowsOpen"] and tvoc_outside > 400:
            messages.append("In diesem Raum sind die Fenster trotz erhöhter Schadstoffbelastung offen.")
        for high_powered_room in high_powered_rooms:
            if room["id"] == high_powered_room["id"]:
                messages.append("In diesem Raum ist der Energieverbrauch um "
                                + str(high_powered_room["difference"]) + "W höher als erwartet.")
                break
        room_copy = room.copy()
        room_copy["status"] = messages
        rooms.append(room_copy)

    return rooms, live_data, raspi_data, live_time
