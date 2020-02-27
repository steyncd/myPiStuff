import models.MqttDevice as MqttDevice


class MqttSwitch(MqttDevice.MqttDevice):
    def __init__(self, name, topic, client, pin):
        super().__init__(name, topic, client)
        self.__pin = pin

    def subscribe_to_topics(self):
        self.getClient().subscribe(self.getCommandTopic())

    def get_pin(self):
        return self.__pin
