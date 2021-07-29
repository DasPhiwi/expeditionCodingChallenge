from pigpio_dht import DHT11, DHT22
import ccs811LIBRARY
from datetime import datetime
import threading


class SensorData:
    def __init__(self):
        self.sensorDHT22 = DHT22(4)
        self.sensorCCS811 = ccs811LIBRARY.CCS811()

        self.temp = 0
        self.humidity = 0
        self.co2 = 0
        self.tvoc = 0
        self.baselineCCS811 = 0
        self.time = datetime.now()

        self.setupCCS811(1)
        self.sensor_thread = threading.Thread(target=self.thread_update_sensordata, daemon=True)
        self.sensor_thread.start()

    def setupCCS811(self, mode=1):
        self.sensorCCS811.configure_ccs811()
        self.sensorCCS811.set_drive_mode(mode)

        if self.sensorCCS811.check_for_error():
            self.sensorCCS811.print_error()
            raise ValueError('Error at setDriveMode.')

        result = self.sensorCCS811.get_base_line()
        self.baselineCCS811 = result

    def thread_update_sensordata(self):
        while True:
            self.time = datetime.now()
            if self.sensorCCS811.data_available():
                self.sensorCCS811.read_logarithm_results()
                self.co2 = self.sensorCCS811.CO2
                self.tvoc = self.sensorCCS811.tVOC
            elif self.sensorCCS811.check_for_error():
                self.sensorCCS811.print_error()

            dht22_result = self.sensorDHT22.read()
            while not dht22_result["valid"]:
                dht22_result = self.sensorDHT22.read()

            self.temp = dht22_result['temp_c']
            self.humidity = dht22_result['humidity']


