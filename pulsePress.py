#!/usr/bin/python3.7
import sys
import RPi.GPIO as g
import time as t
import paho.mqtt.client as mqtt
import subprocess
import os
import configparser
import json

g.setwarnings(False)
g.setmode(g.BCM)

g.setup(27, g.OUT)
g.setup(22, g.OUT)
g.setup(23, g.OUT)
g.setup(24, g.OUT)
g.setup(10, g.IN, pull_up_down=g.PUD_DOWN)
g.setup(9, g.IN, pull_up_down=g.PUD_DOWN)

devices = [27, 22, 23, 24]

for device in devices:
    g.output(device, 1)

startLoopRunning = False
toggleLightRunning = False


def startLoop():
    global startLoopRunning
    startLoopRunning = True
    action = 1
    print("Starting first loop")
    for i in range(30):
        print("Starting device loop " + str(i) + " with action " + str(action))
        for device in devices:
            print("setting device " + str(device) + " to state " + str(action))
            g.output(device, action)
            t.sleep(0.08)

        print("reversing list")
        devices.reverse()
        print("switching action")
        if action == 0:
            action = 1
        else:
            action = 0
    startLoopRunning = False


def toggleLights():
    global toggleLightRunning
    toggleLightRunning = True
    for d in devices:
        if g.input(d) == 1:
            g.output(d, 0)
        else:
            g.output(d, 1)

    t.sleep(1)
    toggleLightRunning = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Hello, Connected to MQTT Broker")


def on_message(client, userdata, message):
    print("handle_command::received command with topic ", message.topic, "and payload ", message.payload)
    if "helloliam/geyser/timer" in message.topic:
        print("geyser timer update command received")
        if message.topic == "helloliam/geyser/timer/1":
            print("Received update for schedule 1")
            updateTimerSettings('1', str(message.payload.decode("utf-8")))
        elif message.topic == "helloliam/geyser/timer/2":
            print("Received update for schedule 2")
            updateTimerSettings('2', str(message.payload.decode("utf-8")))
        elif message.topic == "helloliam/geyser/timer/3":
            print("Received update for schedule 3")
            updateTimerSettings('3', str(message.payload.decode("utf-8")))
        elif message.topic == "helloliam/geyser/timer/4":
            print("Received update for schedule 4")
            updateTimerSettings('4', str(message.payload.decode("utf-8")))
    else:
        action = str(message.payload.decode("utf-8")).strip().lower()
        client.publish("helloliam/geyser/lastcommand", action)
        if action == "on" or action == "1":
            g.output(27, g.LOW)
            print("HandleCommand::on command received")
            client.publish("helloliam/geyser/status", "ON")
            print("HandleCommand::Turning HelloGeyser on")
        elif action == "off" or action == "0":
            g.output(27, g.HIGH)
            print("HandleCommand::off command received")
            client.publish("helloliam/geyser/status", "OFF")
            print("HandleCommand::Turning HelloGeyser off")
        elif action == "toggle":
            print("HandleCommand::toggle command received")
            if g.input(27) == g.HIGH:
                g.output(27, g.LOW)
                client.publish("helloliam/geyser/status", "ON")
            else:
                g.output(27, g.HIGH)
                client.publish("helloliam/geyser/status", "OFF")

            print("HandleCommand::toggling HelloGeyser status")
        elif action == "status":
            print("HandleCommand::Status command received")
            print("HandleCommand::checking status")
            if g.input(27) == g.HIGH:
                client.publish("helloliam/geyser/status", "OFF")
            else:
                client.publish("helloliam/geyser/status", "ON")
        elif action == "gettimer":
            print("HandleCommand::gettimer command received")
            client.publish("helloliam/geyser/timer", json.dumps(parseTimer()))
        elif action == "pulse":
            startLoop()
        elif action == "allon":
            g.output(27, 0)
            g.output(22, 0)
            g.output(23, 0)
            g.output(24, 0)
        elif action == "alloff":
            g.output(27, 1)
            g.output(22, 1)
            g.output(23, 1)
            g.output(24, 1)
        else:
            print("ToggleGeyser::Command not recognized")
            client.publish("helloliam/geyser/status", "Unknown action")
            commands = {
                "on": "Turn Relay 1 on",
                "off": "Turn Relay 1 off",
                "toggle": "Toggle Relay 1 power",
                "allon": "Turn all Relays on",
                "alloff": "Turn all Relays off",
                "gettimer": "Get list of time schedules",
                "status": "Get device status",
                "helloliam/geyser/timer/x": "Update time schedule with {\"Enabled\": false,\"Days\": \"0,2,4\",\"Start\": \"16:54\",\"Stop\": \"16:55\"}"
            }

            client.publish("helloliam/geyser/help", json.loads(commands))


def get_ram():
    try:
        s = subprocess.check_output(["free", "-m"])
        lines = s.splitlines()
        return (int(lines[1].split()[1]), int(lines[2].split()[3]))
    except:
        return 0


def get_process_count():
    try:
        s = subprocess.check_output(["ps", "-e"])
        return len(s.splitlines())
    except:
        return 0


def get_up_stats():
    try:
        s = subprocess.check_output(["uptime"])
        load_split = s.split(b'load average: ')
        load_five = float(load_split[1].split(b', ')[1])
        up = load_split[0]
        up_pos = up.rfind(b', ', 0, len(up) - 4)
        up = up[:up_pos].split(b'up ')[1]
        return (up, load_five)
    except:
        return "", 0


def get_connections():
    try:
        s = subprocess.check_output(["netstat", "-tun"])
        return len([x for x in s.split() if x == b'ESTABLISHED'])
    except:
        return 0


def get_temperature():
    try:
        s = subprocess.check_output(["/opt/vc/bin/vcgencmd", "measure_temp"])
        return float(s.split(b'=')[1][:-3])
    except:
        return 0


def get_ipaddress():
    arg = 'ip route list'
    p = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    ipaddr = split_data[split_data.index(b'src') + 1]
    return ipaddr


def get_cpu_speed():
    f = os.popen('/opt/vc/bin/vcgencmd get_config arm_freq')
    cpu = f.read()
    return cpu


def parseTimer():
    config = configparser.ConfigParser()
    config.read(r'./timer.config')

    timer = {
        "Schedule 1": {
            "Enabled": config.get("timer", "Schedule1Enabled") == "True",
            "Days": config.get("timer", "days1"),
            "Start": config.get("timer", "start1"),
            "Stop": config.get("timer", "stop1")
        },
        "Schedule 2": {
            "Enabled": config.get("timer", "Schedule2Enabled") == "True",
            "Days": config.get("timer", "days2"),
            "Start": config.get("timer", "start2"),
            "Stop": config.get("timer", "stop2")
        },
        "Schedule 3": {
            "Enabled": config.get("timer", "Schedule3Enabled") == "True",
            "Days": config.get("timer", "days3"),
            "Start": config.get("timer", "start3"),
            "Stop": config.get("timer", "stop3")
        },
        "Schedule 4": {
            "Enabled": config.get("timer", "Schedule4Enabled") == "True",
            "Days": config.get("timer", "days4"),
            "Start": config.get("timer", "start4"),
            "Stop": config.get("timer", "stop4")
        }
    }

    return timer


def updateTimerSettings(i, payload):
    print("Updating time settings for schedule " + i + ": " + payload)
    newschedule = json.loads(payload)

    config = configparser.ConfigParser()
    config.read(r'./timer.config')
    config.set("timer", "Schedule" + i + "Enabled", str(newschedule["Enabled"]))
    config.set("timer", "days" + i, newschedule["Days"])
    config.set("timer", "start" + i, newschedule["Start"])
    config.set("timer", "stop" + i, newschedule["Stop"])
    with open('timer.config', 'w') as configfile:
        config.write(configfile)


def runTimer():
    timer = parseTimer()

    for i in range(1, 5):
        schedule = "Schedule " + str(i)
        if timer[schedule]["Enabled"] and t.strftime("%w") in timer[schedule]["Days"]:
            start_time = timer[schedule]["Start"].split(":")
            stop_time = timer[schedule]["Stop"].split(":")
            if t.strftime("%H") == start_time[0] and t.strftime("%M") == start_time[1]:
                print("Start hour and minute match")
                g.output(27, g.LOW)
                t.sleep(60)
            elif t.strftime("%H") == stop_time[0] and t.strftime("%M") == stop_time[1]:
                print("Stop hour and minute match")
                g.output(27, g.HIGH)
                t.sleep(60)


client = mqtt.Client("HelloGeyser")
client.connect("192.168.0.71", 1883)
client.on_connect = on_connect
client.on_message = on_message

client.publish("helloliam/geyser/connection", "Hello! I am connected")
client.subscribe("helloliam/geyser/cmnd")
client.subscribe("helloliam/geyser/timer/1")
client.subscribe("helloliam/geyser/timer/2")
client.subscribe("helloliam/geyser/timer/3")
client.subscribe("helloliam/geyser/timer/4")
client.loop_start()

print('Free RAM: ' + str(get_ram()[1]) + ' (' + str(get_ram()[0]) + ')')
print('Nr. of processes: ' + str(get_process_count()))
print('Up time: ' + str(get_up_stats()[0].decode("utf-8")))
print('Nr. of connections: ' + str(get_connections()))
print('Temperature in C: ' + str(get_temperature()))
print('IP-address: ' + str(get_ipaddress().decode("utf-8")))
print('CPU speed: ' + str(get_cpu_speed()))

while True:
    if g.input(10) == g.HIGH and not startLoopRunning:
        print("starting loop")
        startLoop()

    if g.input(9) == g.HIGH and not toggleLightRunning:
        print("toggling lights")
        toggleLights()

    if int(t.strftime("%M")) % 2 == 0:
        hoststatus = {
            'free_memory': str(get_ram()[1]) + ' (' + str(get_ram()[0]) + ')',
            'processes': str(get_process_count()),
            'up_time': str(get_up_stats()[0].decode("utf-8")),
            'connection_count': str(get_connections()),
            'temperature': str(get_temperature()),
            'ip_address': str(get_ipaddress().decode("utf-8")),
            'cpu_speed': str(get_cpu_speed())
        }

        client.publish("helloliam/geyser/hoststatus", json.dumps(hoststatus))

    runTimer()

g.cleanup()
