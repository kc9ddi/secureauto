from sensor_server.listener import Listener


class TemperatureListener(Listener):
    def receive_message(self, message):
        print message