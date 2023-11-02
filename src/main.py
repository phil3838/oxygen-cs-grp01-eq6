from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
import requests
import json
import time
from crud import Crud, Table


class Main:
    def __init__(self):
        """Setup environment variables and default values."""
        self._hub_connection = None
        self.HOST = "https://hvac-simulator-a23-y2kpq.ondigitalocean.app"  # Setup your host here
        self.TOKEN = "S1rN2enD5p"  # Setup your token here

        self.TICKETS = 2  # Setup your tickets here
        self.T_MAX = 40  # Setup your max temperature here
        self.T_MIN = 10  # Setup your min temperature here
        self.crud = Crud()

    def __del__(self):
        if self._hub_connection != None:
            self._hub_connection.stop()

    def setup(self):
        """Setup Oxygen CS."""
        self.set_sensorhub()

    def start(self):
        """Start Oxygen CS."""
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.", flush=True)
        while True:
            time.sleep(2)

    def set_sensorhub(self):
        """Configure hub connection and subscribe to sensor data events."""
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )

        self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
        self._hub_connection.on_open(lambda: print("||| Connection opened.", flush=True))
        self._hub_connection.on_close(lambda: print("||| Connection closed.", flush=True))
        self._hub_connection.on_error(
            lambda data: print(f"||| An exception was thrown closed: {data.error}", flush=True)
        )

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data on reception."""
        try:
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            date = data[0]["date"]
            temperature = float(data[0]["data"])
            self.take_action(temperature)
            ##  Insert in DB, temperature + timestamp here 
            self.crud.connect()
            self.crud.insert_metric(Table.HVAC, "temperature", temperature)
        except Exception as err:
            print(err, flush=True)

    def take_action(self, temperature):
        """Take action to HVAC depending on current temperature."""
        if float(temperature) >= float(self.T_MAX):
            self.send_action_to_hvac("TurnOnAc")
        elif float(temperature) <= float(self.T_MIN):
            self.send_action_to_hvac("TurnOnHeater")

    def send_action_to_hvac(self, action):
        """Send action query to the HVAC service."""
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{self.TICKETS}")
        details = json.loads(r.text)
        print(details, flush=True)

    def send_event_to_database(self, timestamp, event):
        """Save sensor data into database."""
        try:
            # To implement
            self.crud.connect()
            self.crud.insert_metric(Table.HVAC_EVENTS,"event", event)
            
        except requests.exceptions.RequestException as e:
            # To implement
            pass


if __name__ == "__main__":
    main = Main()
    main.start()
