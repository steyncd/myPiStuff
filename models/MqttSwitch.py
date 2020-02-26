import models.MqttDevice as MqttDevice
import RPi.GPIO as gpio

class MqttSwitch(MqttDevice.MqttDevice) :
    def __init__(self,name,topic,client,pin) :
        super().__init__(name,topic,client)
        self.__pin = pin
        gpio.setmode(gpio.BCM)
        gpio.setup(pin, gpio.OUT)  # GPIO Assign mode
        if gpio.input(pin) == gpio.HIGH:
            self.setStatus("Off")
        else:
            self.setStatus("On")
        self.PostStatus()

    def HandleCommand(self, topic, payload) :
        action = str(payload.decode("utf-8")).strip().lower()
        print("HandleCommand::received command with topic ", topic, "and payload ", payload)
        if action=="on" or action=="1":
            gpio.output(self.__pin, gpio.LOW)
            print("HandleCommand::on command received")
            # self.getClient().publish(self.getStatusTopic,"ON")
            # self.setStatus("On")
            # print("HandleCommand::Turning ",self.getName()," on, pin: " + self.__pin)
        elif action=="off" or action=="0":
            gpio.output(self.__pin, gpio.HIGH)
            print("HandleCommand::off command received")
            # gpio.output(self.__pin, gpio.HIGH)
            # self.getClient().publish(self.getStatusTopic,"ON")
            # self.setStatus("Off")
            # print("HandleCommand::turning " + self.getName() + " off, pin: " + self.__pin)
        elif action=="toggle":
            print("HandleCommand::toggle command received")
            # if gpio.input(self.__pin) == gpio.HIGH:
            #     gpio.output(self.__pin, gpio.LOW)
            # else:
            #     gpio.output(self.__pin, gpio.HIGH)
            #
            # self.setStatus("On" if self.__status == "Off" else "Off")
            # self.getClient().publish(self.getStatusTopic,self.getStatus)
            # print("HandleCommand::toggling " + self.getName() + " status, pin: " + self.__pin)
        elif action=="status":
            print("HandleCommand::Status command received")
            # print("HandleCommand::checking " + self.getName() + " status")
            # if gpio.input(pin) == gpio.HIGH:
            #     self.setStatus("Off")
            # else:
            #     self.setStatus("On")
            # self.PostStatus()
        else:
            print("ToggleGeyser::Command not recognized")
            self.getClient().publish(self.getStatusTopic,"Unknown action")

    def PostStatus(self) :
        print("PostStatus::Updating the " + self.getName() + " status to "+self.getStatus())
        self.getClient().publish(self.getStatusTopic(),self.getStatus())

    def SubscribeToTopics(self) :
        self.getClient().subscribe(self.getCommandTopic())
        self.getClient().subscribe(self.getStatusTopic())
