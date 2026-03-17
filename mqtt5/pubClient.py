
import paho.mqtt as client
import paho.mqtt.publish as publish
import socket
from time import *

"MQTTBOKER = socket.gethostbyname(host.docker.internal"
"i changed for the compatibility because the ip can change , its depends on the place you are"
MQTTBOKER = "127.0.0.1"        
Topic = "satelliteSS/radio"

"""
This script sends the commands provided in Table 1 of DOC-15-25001 Satellite Subsystem Lab#1,
with a 6 seconds interval between commands.
"""


# Get default set mode:
msg = 0x0102    
publish.single(Topic,msg,hostname = MQTTBOKER)
sleep(6)

# Set the radio to mode 1 - operational mode
msg = 0x0101
publish.single(Topic,msg,hostname = MQTTBOKER)
sleep(6)

# Set the radio to mode 0 - standby
msg = 0x0100
publish.single(Topic,msg,hostname = MQTTBOKER)
sleep(6)

# Get "firmware" version
msg = 0x0103
publish.single(Topic,msg,hostname = MQTTBOKER)
sleep(6)