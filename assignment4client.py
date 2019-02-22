import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

def on_connect(client, userdata, flags, rc):
	if rc == 5:
		print("\nInvalid username or password.\n")
	elif rc == 0:
		print("Welcome to the Traffic Lights Server")

def on_message(client, userdata, message):
	print("\n" + str(message.payload))

# Setup the client
client = mqtt.Client(client_id="Client")
client.username_pw_set(username="traffic", password="lights")
client.on_message = on_message
client.on_connect = on_connect

# Connect to the Broker
client.connect("127.0.0.1", port = 1883, keepalive=60, bind_address="")
menu = "n"

while menu.lower() != "q":
	print("\n\n\n----------  MENU  ----------")
	print("\nA - Send a car")
	print("B - Change Lights")
	print("C - Status Request")
	print("Q - Quit\n")
	menu = raw_input("What would you like to do: ")
	if menu.lower() == "a":
		direction = raw_input("What direction is the car coming from: ")
		if direction.lower() == "n":
			# Send message to Broker
			client.publish("traffic/direction", "n", qos=0, retain=False)
		elif direction.lower() == "s":
			# Send message to Broker
			client.publish("traffic/direction", "s", qos=0, retain=False)
		elif direction.lower() == "e":
			# Send message to Broker
			client.publish("traffic/direction", "e", qos=0, retain=False)
		elif direction.lower() == "w":
			# Send message to Broker
			client.publish("traffic/direction", "w", qos=0, retain=False)
	elif menu.lower() == "b":
		style = raw_input("What style would you like the lights (US/UK): ")
		if style.lower() == "us":
			# Send message to Broker
			client.publish("traffic/lights", "us", qos=0, retain=False)
		elif style.lower() == "uk":
			# Send message to Broker
			client.publish("traffic/lights", "uk", qos=0, retain=False)
	elif menu.lower() == "c":
		client.publish("traffic/status", "status", qos=0, retain=False)
		client.subscribe("traffic/reply", 0)
		client.loop_start()
		time.sleep(1)


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
