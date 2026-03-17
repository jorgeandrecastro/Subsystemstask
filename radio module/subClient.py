"""
MQTT subscribing client using subscribe callback function
Reference:
https://pypi.org/project/paho-mqtt/

"""
import sys
import subprocess
import socket
from datetime import *

try:
    import paho.mqtt.client as mqtt
    import paho.mqtt.subscribe as subscribe
except ImportError:
    results = subprocess.run([sys.executable, "-m", "pip", "install", "paho-mqtt==1.6.1"],check=True,capture_output=True,text=True)
    print(f"paho-mqtt 1.6.1 installed successfully: {results.stdout}")
except subprocess.CalledProcessError as e:
    print(f"Failed to install paho-mqtt 1.6.1: {e.std.err}")
    sys.exit(1)
finally:
    import paho.mqtt.client as mqtt
    import paho.mqtt.subscribe as subscribe 
    
MQTTBOKER = socket.gethostbyname("host.docker.internal")
Topic = "satelliteSS/#"

def on_message(client,userdata,message):
    print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Topic: {message.topic} | message: {message.payload.decode()}")
    
    
def main():
    try:
        client = mqtt.Client
        subscribe.callback(on_message,Topic,hostname = MQTTBOKER)
    except KeyboardInterrupt:
        print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Exiting.")


if __name__ == "__main__":
    main()