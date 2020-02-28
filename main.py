import RPi.GPIO as GPIO
import configparser
import services.MyMqttService as mqttService
import models.MqttSwitch as Switch
import paho.mqtt.client as mqtt
import time

GPIO.VERBOSE = False

try:
    def handle_command(device, topic, payload):
        action = str(payload.decode("utf-8")).strip().lower()
        print("handle_command::received command with topic ", topic, "and payload ", payload)
        if action == "on" or action == "1":
            GPIO.output(device.get_pin(), GPIO.LOW)
            print("HandleCommand::on command received")
            device.getClient().publish(device.getStatusTopic(), "ON")
            device.setStatus("On")
            print("HandleCommand::Turning ", device.getName(), " on, pin: " + device.get_pin())
        elif action == "off" or action == "0":
            GPIO.output(device.get_pin(), GPIO.HIGH)
            print("HandleCommand::off command received")
            device.getClient().publish(device.getStatusTopic(), "Off")
            device.setStatus("Off")
            print("HandleCommand::turning " + device.getName() + " off, pin: " + device.get_pin())
        elif action == "toggle":
            print("HandleCommand::toggle command received")
            if GPIO.input(device.get_pin()) == GPIO.HIGH:
                GPIO.output(device.get_pin(), GPIO.LOW)
            else:
                GPIO.output(device.get_pin(), GPIO.HIGH)

            device.setStatus("On" if device.getStatus() == "Off" else "Off")
            device.getClient().publish(device.getStatusTopic(), device.getStatus())
            print("HandleCommand::toggling " + device.getName() + " status, pin: " + device.get_pin())
        elif action == "status":
            print("HandleCommand::Status command received")
            print("HandleCommand::checking " + device.getName() + " status")
            if GPIO.input(device.get_pin) == GPIO.HIGH:
                device.setStatus("Off")
            else:
                device.setStatus("On")
            post_status(device)
        else:
            print("ToggleGeyser::Command not recognized")
            device.getClient().publish(device.getStatusTopic(), "Unknown action")


    def post_status(device):
        print("PostStatus::Updating the " + device.getName() + " status to " + device.getStatus())
        device.getClient().publish(device.getStatusTopic(), device.getStatus())


    def on_connect(client, userdata, flags, rc):
        try:
            if rc == 0:
                print("on_connect::Successfully connected to HelloLiam MQTT Broker ", rc)
            else:
                print("on_connect::Bad connection Returned code=", rc)
        except Exception as err:
            print("on_connect::Something went wrong - " + err)


    def on_subscribe():
        print("Subscribed")


    def on_message(client, userdata, message):
        print("on_message::message received  ", str(message.payload.decode("utf-8")),
              "topic", message.topic, "retained ", message.retain, " by ", userdata)
        if message.retain == 1:
            print("on_message::This is a retained message")

        if myGeyser.getTopic() in message.topic:
            print("on_message::Topic matches geyser topic")
            handle_command(myGeyser, message.topic, message.payload)
        elif switch2.getTopic() in message.topic:
            print("on_message::Topic matches switch2 topic")
            handle_command(switch2, message.topic, message.payload)
        elif switch3.getTopic() in message.topic:
            print("on_message::Topic matches switch3 topic")
            handle_command(switch3, message.topic, message.payload)
        elif switch4.getTopic() in message.topic:
            print("on_message::Topic matches switch4 topic")
            handle_command(switch4, message.topic, message.payload)
        else:
            print("on_message::Topic not matched to device")


    def on_publish(client, userdata, mid):
        print("Messaged published: " + str(mid))


    configParser = configparser.RawConfigParser()
    configFilePath = r'./settings.config'
    configParser.read(configFilePath)

    mqtt_client = mqtt.Client(configParser.get('settings', 'mqtt_client'))
    mqtt_client.on_connect = on_connect
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_message = on_message
    mqtt_client.on_publish = on_publish

    queueService = mqttService.MyMqttService(
        mqtt_client,
        configParser.get('settings', 'mqtt_client'),
        configParser.get('settings', 'mqtt_host'),
        int(configParser.get('settings', 'mqtt_port')),
        configParser.get('settings', 'mqtt_client') + "/")

    time.sleep(4)

    myGeyser = Switch.MqttSwitch(
        configParser.get('settings', 'device1_name'),
        configParser.get('settings', 'device1_topic'),
        mqtt_client,
        int(configParser.get('settings', 'device1_pin')))
    switch2 = Switch.MqttSwitch(
        configParser.get('settings', 'device2_name'),
        configParser.get('settings', 'device2_topic'),
        mqtt_client,
        int(configParser.get('settings', 'device2_pin')))
    switch3 = Switch.MqttSwitch(
        configParser.get('settings', 'device3_name'),
        configParser.get('settings', 'device3_topic'),
        mqtt_client,
        int(configParser.get('settings', 'device3_pin')))
    switch4 = Switch.MqttSwitch(
        configParser.get('settings', 'device4_name'),
        configParser.get('settings', 'device4_topic'),
        mqtt_client,
        int(configParser.get('settings', 'device4_pin')))

    devices = [myGeyser, switch2, switch3, switch4]

    for this_device in devices:
        GPIO.setup(this_device.get_pin(), GPIO.OUT)
        this_device.subscribe_to_topics()
        if GPIO.input(this_device.get_pin()) == GPIO.LOW:
            this_device.setStatus("On")
        else:
            this_device.setStatus("Off")

    while True:
        if not queueService.get_connected():
            print("I am not connected...but I am probably still trying.")
        # else:
        #    print("I am not connected...but I am probably still trying.")

        time.sleep(15)
finally:
    print("Cleaning up GPIO ports")
    GPIO.cleanup()
