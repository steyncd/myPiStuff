import models.Device as Device


class MqttDevice(Device.Device):
    __commandTopic = "cmnd"
    __statusTopic = "status"
    __connectionTopic = "status/connection"
    __status = "Standby"

    def __init__(self, name, topic, client):
        super().__init__(name)
        self.__topic = topic
        self.__mqttClient = client

    def getTopic(self):
        return self.__topic

    def getCommandTopic(self):
        return self.__topic + self.__commandTopic

    def getStatusTopic(self):
        return self.__topic + self.__statusTopic

    def getConnectionTopic(self):
        return self.__topic + self.__connectionTopic

    def getStatus(self):
        return self.__status

    def setStatus(self, status):
        self.__status = status

    def getClient(self):
        return self.__mqttClient
