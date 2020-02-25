import models.MqttDevice as MqttDevice
import RPi.GPIO as GPIO

class MqttSwitch(MqttDevice.MqttDevice) :
    def __init__(self,name,topic,client) :
        super().__init__(name,topic,client)
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(10, GPIO.OUT)
        if GPIO.output(10) == GPIO.HIGH
            self.setStatus("Off")
        else
            self.setStatus("On")

    def HandleCommand(self, topic, payload) :
        action = str(payload.decode("utf-8")).strip().lower()
        print("HandleCommand::received command with topic ", topic, "and payload ", payload)
        #command
        if self.getCommandTopic() in topic :
            if action=="on" or action=="1":
                print("HandleCommand::Turning ",self.getName()," on")
                self.getClient().publish(self.getStatusTopic,"ON")
                self.setStatus("On")
                self.PostStatus()
                GPIO.output(10, GPIO.LOW)
            elif action=="off" or action=="0":
                print("HandleCommand::turning geyser off")
                self.getClient().publish(self.getStatusTopic,"ON")
                self.setStatus("Off")
                self.PostStatus()
                GPIO.output(10, GPIO.HIGH)
            elif action=="toggle":
                print("HandleCommand::toggling geyser status")
                self.setStatus("On" if self.__status == "Off" else "Off")
                self.getClient().publish(self.getStatusTopic,self.getStatus)
                self.PostStatus()
                
                if GPIO.output(10) == GPIO.HIGH:
                    GPIO.output(10, GPIO.LOW)
                else
                    GPIO.output(10, GPIO.HIGH)
            elif action=="status":
                print("HandleCommand::checking geyser status")
                self.PostStatus()
            else:
                print("ToggleGeyser::Command not recognized")
                self.getClient().publish(self.getStatusTopic,"Unknown action")
        elif self.getStatusTopic() in topic :
            self.PostStatus()

    def PostStatus(self) :
        print("PostStatus::Updating the device status to "+self.getStatus())
        self.getClient().publish(self.getStatusTopic(),self.getStatus())

    def SubscribeToTopics(self) :
        self.getClient().subscribe(self.getCommandTopic())
        self.getClient().subscribe(self.getStatusTopic())