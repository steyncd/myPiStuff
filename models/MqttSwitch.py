import models.MqttDevice as MqttDevice

class MqttSwitch(MqttDevice.MqttDevice) :
    def __init__(self,name,topic,client,pin,gpio) :
        super().__init__(name,topic,client)
        self.__pin = pin
        if gpio.input(pin) == gpio.HIGH:
            self.setStatus("Off")
        else:
            self.setStatus("On")
        self.PostStatus()

    def HandleCommand(self, topic, payload, gpio) :
        action = str(payload.decode("utf-8")).strip().lower()
        print("HandleCommand::received command with topic ", topic, "and payload ", payload)
        #command
        #if self.getCommandTopic() in topic :
        if action=="on" or action=="1":
            gpio.setup(self.__pin,gpio.OUT)
            gpio.output(self.__pin, gpio.LOW)
            self.getClient().publish(self.getStatusTopic,"ON")
            self.setStatus("On")
            print("HandleCommand::Turning ",self.getName()," on, pin: " + self.__pin)
        elif action=="off" or action=="0":
            gpio.output(self.__pin, gpio.HIGH)
            self.getClient().publish(self.getStatusTopic,"ON")
            self.setStatus("Off")
            print("HandleCommand::turning " + self.getName() + " off, pin: " + self.__pin)
        elif action=="toggle":
            if gpio.input(self.__pin) == gpio.HIGH:
                gpio.output(self.__pin, gpio.LOW)
            else:
                gpio.output(self.__pin, gpio.HIGH)

            self.setStatus("On" if self.__status == "Off" else "Off")
            self.getClient().publish(self.getStatusTopic,self.getStatus)
            print("HandleCommand::toggling " + self.getName() + " status, pin: " + self.__pin)
        elif action=="status":
            print("HandleCommand::checking " + self.getName() + " status")
            if gpio.input(pin) == gpio.HIGH:
                self.setStatus("Off")
            else:
                self.setStatus("On")
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
