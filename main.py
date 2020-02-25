import paho.mqtt.client as mqtt
import time as time
import services.MyMqttService as mqttService
import models.Device as Device
import models.MqttDevice as MqttDevice
import models.MqttSwitch as Switch
from multiprocessing import Pool

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
        myGeyser.HandleCommand(message.topic, message.payload)

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

queueService = mqttService.MyMqttService("HelloLiam", "127.0.0.1", 1883, "helloliam/", on_connect, on_subscribe, on_message, on_publish)
queueService.connectToBroker()
client = queueService.getClient()

myGeyser = Switch.MqttSwitch("Geyser","helloliam/geyser/", client)
myGeyser.continuousUpdate = True
myGeyser.SubscribeToTopics()

client.loop_forever()
