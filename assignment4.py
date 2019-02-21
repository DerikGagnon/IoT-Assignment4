import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from Queue import *

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

# Initialize all as false
GPIO.output(ns_red, False)
GPIO.output(ns_yellow, False)
GPIO.output(ns_green, False)

GPIO.output(ew_red, False)
GPIO.output(ew_yellow, False)
GPIO.output(ew_green, False)

global queueN
global queueS
global queueE
global queueW
global timer2
global usLight
usLight = Queue(maxsize=0)
timer2 = 0
queueN = Queue(maxsize=0)
queueS = Queue(maxsize=0)
queueE = Queue(maxsize=0)
queueW = Queue(maxsize=0)

def switch_lights():
	if not usLight.empty():
		if GPIO.input(ns_green) == True:
			GPIO.output(ns_green, False)
			GPIO.output(ns_yellow, True)
			time.sleep(1)
			GPIO.output(ns_yellow, False)
			GPIO.output(ns_red, True)
			time.sleep(1)
			GPIO.output(ew_red, False)
			GPIO.output(ew_green, True)
			for i in range(0,2):
				print(str(queueE.qsize()), " cars in queueE - Switch Lights")
				print(str(queueW.qsize()), " cars in queueW - Switch Lights")
				time.sleep(1)
				
				if not queueE.empty():
					queueE.get()
				if not queueW.empty():
					queueW.get()
		else:
			GPIO.output(ew_green, False)
			GPIO.output(ew_yellow, True)
			time.sleep(1)
			GPIO.output(ew_yellow, False)
			GPIO.output(ew_red, True)
			time.sleep(1)
			GPIO.output(ns_green, True)
			GPIO.output(ns_red, False)
			for i in range(0,5):
				if not queueN.empty():
					queueN.get()
				if not queueS.empty():
					queueS.get()
				time.sleep(1)
	else:
		# UK Light Scheme
		print("UK")
		if GPIO.input(ns_green) == True:
			GPIO.output(ns_green, False)
			GPIO.output(ns_yellow, True)
			time.sleep(1)
			GPIO.output(ns_yellow, False)
			GPIO.output(ns_red, True)
			time.sleep(1)
			GPIO.output(ew_yellow, True)
			time.sleep(1)
			GPIO.output(ew_red, False)
			GPIO.output(ew_yellow, False)
			GPIO.output(ew_green, True)
			for i in range(0,2):
				print(str(queueE.qsize()), " cars in queueE - Switch Lights")
				print(str(queueW.qsize()), " cars in queueW - Switch Lights")
				time.sleep(1)
				
				if not queueE.empty():
					queueE.get()
				if not queueW.empty():
					queueW.get()
		else:
			GPIO.output(ew_green, False)
			GPIO.output(ew_yellow, True)
			time.sleep(1)
			GPIO.output(ew_yellow, False)
			GPIO.output(ew_red, True)
			time.sleep(1)
			GPIO.output(ns_yellow, True)
			time.sleep(1)
			GPIO.output(ns_yellow, False)
			GPIO.output(ns_red, False)
			GPIO.output(ns_green, True)
			for i in range(0,5):
				if not queueN.empty():
					queueN.get()
				if not queueS.empty():
					queueS.get()
				time.sleep(1)
			

# Start program with ns dominance
GPIO.output(ns_green, True)
GPIO.output(ew_red, True)
usLight.put("USA")

def on_message(client, userdata, message):
	print("Message Topic: ", message.topic)
	print("Message Payload: ", str(message.payload))
	if message.topic == "traffic/direction":
		if str(message.payload) == "n":
			queueN.put(str(message.payload))
		elif str(message.payload) == "s":
			queueS.put(str(message.payload))
		elif str(message.payload) == "e":
			queueE.put(str(message.payload))
		elif str(message.payload) == "w":
			queueW.put(str(message.payload))
	elif message.topic == "traffic/lights":
		if str(message.payload) == "us":
			usLight.put("USA")
		elif str(message.payload) == "uk":
			while not usLight.empty():
				usLight.get()
	elif message.topic == "traffic/status":
		if str(message.payload) == "status":
			# Send message to publisher
			print(str(queueE.qsize()), " cars waiting from the East")
			print(str(queueW.qsize()), " cars waiting from the West")
			print(str(queueN.qsize()), " cars waiting from the North")
			print(str(queueS.qsize()), " cars waiting from the South")
			if GPIO.input(ns_green) == True:
				print("Green light for North/South")
				print("Red light for East/West")
			else:
				print("Green light for East/West")
				print("Red light for North/South")
			if usLight.empty():
				print("Light Style: UK")
			else:
				print("Light Style: US")

client = mqtt.Client(client_id="Server")
client.connect("127.0.0.1", port = 1883, keepalive=60, bind_address="")
client.subscribe("traffic/direction", qos=0)
# [("my/topic", 0), ("another/topic", 2)]

client.on_message = on_message
client.loop_start()
for i in range (0,5):
		time.sleep(1)
while True:
	if not queueE.empty() or not queueW.empty() and GPIO.input(ns_green) == True:
		switch_lights()
	elif queueE.empty() and queueW.empty() and GPIO.input(ew_green) == True:
		print("Switch Lights")
		switch_lights()
	elif not queueE.empty() or not queueW.empty() and GPIO.input(ew_green) == True:
		timer2 = 0
		while not queueE.empty() or not queueW.empty() and timer2 != 3:
			print(str(queueE.qsize()), " cars in queueE")
			print(str(queueW.qsize()), " cars in queueW")
			if not queueE.empty():
				queueE.get()
			if not queueW.empty():
				queueW.get() 
			time.sleep(1)
			timer2 += 1
		print(str(queueE.qsize()), " cars in queueE")
		print(str(queueW.qsize()), " cars in queueW")
		print("Switch Lights")
		
		switch_lights()

GPIO.cleanup()
client.disconnect()
