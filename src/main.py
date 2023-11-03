"""
This module serves to fetch the data and insert them in the database.
"""
import json
import time
import logging
import requests

from signalrcore.hub_connection_builder import HubConnectionBuilder


class Main:
    """
    This is the main?? class responsible for managing connections and orchestrating
    other operations.
    """

    def __init__(self):
        """Setup environment variables and default values."""
        self._hub_connection = None
        self.host = "https://hvac-simulator-a23-y2kpq.ondigitalocean.app"  # Setup your host here
        self.token = "S1rN2enD5p"  # Setup your token here

        self.tickets = 2  # Setup your tickets here
        self.t_max = 40  # Setup your max temperature here
        self.t_min = 10  # Setup your min temperature here
        self.database = None  # Setup your database here

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def setup(self):
        """Setup Oxygen CS"""
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
            .with_url(f"{self.host}/SensorHub?token={self.token}")
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
        self._hub_connection.on_open(
            lambda: print("||| Connection opened.", flush=True)
        )
        self._hub_connection.on_close(
            lambda: print("||| Connection closed.", flush=True)
        )
        self._hub_connection.on_error(
            lambda data: print(
                f"||| An exception was thrown closed: {data.error}", flush=True
            )
        )

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data on reception."""
        try:
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            date = data[0]["date"]
            temperature = float(data[0]["data"])
            self.take_action(temperature)
            ##  Insert in DB, temperature + timestamp here
        except Exception as err:
            print(err, flush=True)

    def take_action(self, temperature):
        """Take action to HVAC depending on current temperature."""
        if float(temperature) >= float(self.t_max):
            self.send_action_to_hvac("TurnOnAc")
        elif float(temperature) <= float(self.t_min):
            self.send_action_to_hvac("TurnOnHeater")

    def send_action_to_hvac(self, action):
        """Send action query to the HVAC service."""
        r = requests.get(f"{self.host}/api/hvac/{self.token}/{action}/{self.tickets}")
        details = json.loads(r.text)
        print(details, flush=True)

    def send_event_to_database(self, timestamp, event):
        """Save sensor data into database."""
        try:
            # To implement
            pass
        except requests.exceptions.RequestException as e:
            # To implement
            pass


if __name__ == "__main__":
    main = Main()
    main.start()
