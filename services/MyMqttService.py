import paho.mqtt.client as mqtt
import time


class MyMqttService:
    connected = False

    def __init__(self, client_name, host, port, topic, on_connect, on_subscribe, on_message, on_publish):
        self.__name = client_name
        self.__host = host
        self.__port = port
        self.__topic = topic
        self.on_message = on_message
        self.on_connect = on_connect
        self.on_subscribe = on_subscribe
        self.on_publish = on_publish
        self.__client = mqtt.Client(client_name)
        # bind callbacks
        self.__client.on_connect = on_connect
        self.__client.on_subscribe = on_subscribe
        self.__client.on_message = on_message
        self.__client.on_publish = on_publish

    def connect_to_broker(self, attempts=10):
        print("MyMqttService::connectToBroker - Connecting to ", self.__host, " on port ", self.__port)
        current_attempt = 1
        while not self.connected and current_attempt <= attempts:
            try:
                print("Connection attempt number " + str(current_attempt))
                current_attempt += 1
                self.__client.connect(self.__host, self.__port)
                self.__client.publish(self.__topic + "connection/status", "Hello! I am connected")
                self.connected = True
                time.sleep(3)
            except ConnectionRefusedError:
                print("Connection refused, trying again")
            except ConnectionError:
                print("Something went wrong while trying to connect, trying again")

    def get_client(self):
        return self.__client
