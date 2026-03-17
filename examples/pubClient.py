
import paho.mqtt as client
import paho.mqtt.publish as publish
import socket


MQTTBOKER = socket.gethostbyname("host.docker.internal")
Topic = "satelliteSS/mqttTest"

msg = "MQTT clients testing."
publish.single(Topic,msg,hostname = MQTTBOKER)