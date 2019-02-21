import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Setup the client
client = mqtt.Client(client_id="Client")

# Connect to the Broker
client.connect("127.0.0.1", port = 1883, keepalive=60, bind_address="")

input = raw_input("What direction is a car coming from? ")

while input.lower() != "q":
	if input.lower() == "n":
		# Send message to Broker
		client.publish("traffic", "n", qos=0, retain=False)
	elif input.lower() == "s":
		# Send message to Broker
		client.publish("traffic", "s", qos=0, retain=False)
	elif input.lower() == "e":
		# Send message to Broker
		client.publish("traffic", "e", qos=0, retain=False)
	elif input.lower() == "w":
		# Send message to Broker
		client.publish("traffic", "w", qos=0, retain=False)
	elif input.lower() == "us":
		# Send message to Broker
		client.publish("traffic", "us", qos=0, retain=False)
	elif input.lower() == "uk":
		# Send message to Broker
		client.publish("traffic", "uk", qos=0, retain=False)
	input = raw_input("What direction is a car coming from? ")

# client = mqtt.Client(client_id="Derik")
# client.connect("127.0.0.1", port = 1883, keepalive=60, bind_address="")
# client.publish("traffic", 10, qos=0, retain=False)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# pin labels for each of the lights
ns_red = 18
ns_yellow = 23
ns_green = 24

ew_red = 25
ew_yellow = 8
ew_green = 7

# Setup GPIO pins
GPIO.setup(ns_red, GPIO.OUT)
GPIO.setup(ns_yellow, GPIO.OUT)
GPIO.setup(ns_green, GPIO.OUT)

GPIO.setup(ew_red, GPIO.OUT)
GPIO.setup(ew_yellow, GPIO.OUT)
GPIO.setup(ew_green, GPIO.OUT)

GPIO.cleanup()
