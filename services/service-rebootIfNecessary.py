#!/usr/bin/python
import paho.mqtt.client as mqtt
import argparse
import signal
import os
import time

parser = argparse.ArgumentParser(description='reboot the raspberry if no new value incomes from a sensor')
parser.add_argument('service_name', metavar='service_name', help='name of the current service')
parser.add_argument('measure_in', metavar='measure_in', help='measure path given')
parser.add_argument('delay', metavar='delay', help='delay without two measures to reboot (in min)', nargs='?', default="30")
parser.add_argument('hostname', metavar='hostname', help='hostname of mqtt server', nargs='?', default="0.0.0.0")
parser.add_argument('port', metavar='port', help='port of mqtt server', nargs='?', default="1883")
args = parser.parse_args()

previous_value = time.time()
run = True

def on_connect(client, userdata, flags, rc):
    client.subscribe(args.measure_in)

def on_message(client, userdata, msg):
    global previous_value
    previous_value = time.time()

def signal_handler(sig, frame):
    if sig is not signal.SIGUSR1:
        print "Ending and cleaning up"
        global run
        run = False
        client.disconnect()

def reboot_if_needed():
    now = time.time()
    if (previous_value + int(args.delay) * 60 < now):
        os.system("shutdown -r +2 reboot from domotik")
        global run
        run = False
        client.disconnect()

signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(args.hostname, int(args.port), 60)

while run:
    client.loop()
    reboot_if_needed()
