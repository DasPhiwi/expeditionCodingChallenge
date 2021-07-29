Requirements:
Python3 with the Packages Flask and pigpio_dht running on the Raspi

Startup:
Copy the files in the raspi folder to a folder on the Raspi
Start the Flask-App on the Raspi ("python3 app.py")
The API should be available on the local net under "[IP_OF_RASPI]:5000/sensordata"

Copy that URL to the config.ini file in the main project