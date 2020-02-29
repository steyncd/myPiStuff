
import time


class MyMqttService:
    connected = False

    def __init__(self, client, client_name, host, port, topic):
        self.__client = client
        self.__name = client_name
        self.__host = host
        self.__port = port
        self.__topic = topic
        self.connect_to_broker(10)

    def connect_to_broker(self, attempts=10):
        print("MyMqttService::connectToBroker - Connecting to ", self.__host, " on port ", self.__port)
        current_attempt = 1
        while not self.connected and current_attempt <= attempts:
            try:
                print("Connection attempt number " + str(current_attempt))
                current_attempt += 1
                self.__client.connect(self.__host, self.__port)
                self.__client.loop_start()
                self.connected = True
            except ConnectionRefusedError:
                print("Connection refused, trying again")
                time.sleep(3)
            except ConnectionError:
                print("Something went wrong while trying to connect, trying again")
                time.sleep(3)

    def get_client(self):
        return self.__client

    def get_connected(self):
        return self.connected
