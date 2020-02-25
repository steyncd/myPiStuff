import paho.mqtt.client as mqtt
import time as time
import services.MyMqttService as mqttService
import models.Device as Device
import models.MqttDevice as MqttDevice
import models.MqttSwitch as Switch
from multiprocessing import Pool
import RPi.GPIO as GPIO

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("on_connect::Successfully connected to HelloLiam MQTT Broker ",rc)
        #if __name__ == '__main__':
         #   pool = Pool(processes=1)              # Start a worker processes.
         #   pool.apply_async(myGeyser.PostStatus) #
    else:
        print("on_connect::Bad connection Returned code=",rc)

def on_subscribe():
    print("Subscribed")

def on_message(client, userdata, message):
    print("on_message::message received  ",str(message.payload.decode("utf-8")),\
          "topic",message.topic,"retained ",message.retain)
    if message.retain==1:
        print("on_message::This is a retained message")
    
    if myGeyser.getTopic() in message.topic :
        print("on_message::Topic matches geyser topic")
        myGeyser.HandleCommand(message.topic, message.payload, GPIO)
    elif switch2.getTopic() in message.topic :
        print("on_message::Topic matches switch2 topic")
        switch2.HandleCommand(message.topic, message.payload, GPIO)
    elif switch3.getTopic() in message.topic :
        print("on_message::Topic matches switch3 topic")
        switch3.HandleCommand(message.topic, message.payload, GPIO)
    elif switch4.getTopic() in message.topic :
        print("on_message::Topic matches switch4 topic")
        switch4.HandleCommand(message.topic, message.payload, GPIO)
    else :
        print("on_message::Topic not matched to device")

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM)

queueService = mqttService.MyMqttService("HelloLiam", "127.0.0.1", 1883, "helloliam/", on_connect, on_subscribe, on_message, on_publish)
queueService.connectToBroker()
client = queueService.getClient()

myGeyser = Switch.MqttSwitch("Geyser","helloliam/geyser/", client, 27, GPIO)
myGeyser.SubscribeToTopics()

switch2 = Switch.MqttSwitch("Switch2","helloliam/switch2/", client, 22, GPIO)
switch2.SubscribeToTopics()

switch3 = Switch.MqttSwitch("Switch3","helloliam/swtich3/", client, 23, GPIO)
switch3.SubscribeToTopics()

switch4 = Switch.MqttSwitch("Switch4","helloliam/switch4/", client, 24, GPIO)
switch4.SubscribeToTopics()

GPIO.cleanup()
client.loop_forever()
