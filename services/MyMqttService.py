
import paho.mqtt.client as mqtt

class MyMqttService :
    def __init__(self, clientName, host, port, topic, on_connect, on_subscribe, on_message, on_publish) :
        self.__name = clientName
        self.__host = host
        self.__port = port
        self.__topic = topic
        self.on_message = on_message
        self.on_connect = on_connect
        self.on_subscribe = on_subscribe
        self.on_publish = on_publish
        self.__client = mqtt.Client(clientName)
        #bind callbacks
        self.__client.on_connect=on_connect
        self.__client.on_subscribe=on_subscribe
        self.__client.on_message=on_message
        self.__client.on_publish=on_publish

    def connectToBroker(self) :
        print("MyMqttService::connectToBroker - Connecting to ", self.__host," on port ", self.__port)
        self.__client.connect(self.__host, self.__port)     
        self.__client.publish(self.__topic+"connection/status", "Hello! I am connected") 

    def getClient(self) :
        return self.__client

    
