import models.MqttDevice as MqttDevice

class MqttSwitch(MqttDevice.MqttDevice) :
    def __init__(self,name,topic,client,pin,gpio) :
        super().__init__(name,topic,client)
        self.__pin = pin
        self.__gpio = gpio
        gpio.setup(pin, gpio.OUT)
        if gpio.input(pin) == gpio.HIGH:
            self.setStatus("Off")
        else:
            self.setStatus("On")

    def HandleCommand(self, topic, payload) :
        action = str(payload.decode("utf-8")).strip().lower()
        print("HandleCommand::received command with topic ", topic, "and payload ", payload)
        #command
        #if self.getCommandTopic() in topic :
        if action=="on" or action=="1":
            self.__gpio.output(self.__pin, self.__gpio.LOW)
            self.getClient().publish(self.getStatusTopic,"ON")
            self.setStatus("On")
            print("HandleCommand::Turning ",self.getName()," on, pin: " + self.__pin)
        elif action=="off" or action=="0":
            self.__gpio.output(self.__pin, self.__gpio.HIGH)
            self.getClient().publish(self.getStatusTopic,"ON")
            self.setStatus("Off")
            print("HandleCommand::turning " + self.getName() + " off, pin: " + self.__pin)
        elif action=="toggle":
            if self.__gpio.input(self.__pin) == self.__gpio.HIGH:
                self.__gpio.output(self.__pin, self.__gpio.LOW)
            else:
                self.__gpio.output(self.__pin, self.__gpio.HIGH)

            self.setStatus("On" if self.__status == "Off" else "Off")
            self.getClient().publish(self.getStatusTopic,self.getStatus)
            print("HandleCommand::toggling " + self.getName() + " status, pin: " + self.__pin)
        elif action=="status":
            print("HandleCommand::checking " + self.getName() + " status")
            self.PostStatus()
        else:
            print("ToggleGeyser::Command not recognized")
            self.getClient().publish(self.getStatusTopic,"Unknown action")

    def PostStatus(self) :
        print("PostStatus::Updating the " + self.getName() + " status to "+self.getStatus())
        self.getClient().publish(self.getStatusTopic(),self.getStatus())

    def SubscribeToTopics(self) :
        self.getClient().subscribe(self.getCommandTopic())
        self.getClient().subscribe(self.getStatusTopic())
