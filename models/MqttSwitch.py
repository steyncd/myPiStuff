import models.MqttDevice as MqttDevice

class MqttSwitch(MqttDevice.MqttDevice) :
    def __init__(self,name,topic,client) :
        super().__init__(name,topic,client)

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
            elif action=="off" or action=="0":
                print("HandleCommand::turning geyser off")
                self.getClient().publish(self.getStatusTopic,"ON")
                self.setStatus("Off")
                self.PostStatus()
            elif action=="toggle":
                print("HandleCommand::toggling geyser status")
                self.setStatus("On" if self.__status == "Off" else "Off")
                self.getClient().publish(self.getStatusTopic,self.getStatus)
                self.PostStatus()
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