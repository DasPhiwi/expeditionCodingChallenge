from flask import Flask
from sensordata import SensorData

app = Flask(__name__)

sensordata_instance = SensorData()

@app.get('/sensordata')
def index():
    return {
                "time": sensordata_instance.time,
                "temp": sensordata_instance.temp,
                "humidity": sensordata_instance.humidity,
                "co2": sensordata_instance.co2,
                "tvoc": sensordata_instance.tvoc
            }

if __name__ == '__main__':
    app.run(host='0.0.0.0')
