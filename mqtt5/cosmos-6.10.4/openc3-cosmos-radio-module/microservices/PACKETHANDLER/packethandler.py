import time
import sys
import socket
import struct
import logging
import paho.mqtt.publish as publish

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

UDP_PORT = 8080
host = "0.0.0.0"
MQTT_BROKER = "host.docker.internal"
MQTT_PORT = 1883
Topic = "satelliteSS/radio"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    sock.bind((host, UDP_PORT))
    logger.info(f"PacketHandler listening on UDP {UDP_PORT}")
except Exception as e:
    logger.error(f"Could not bind: {e}")
    sys.exit(1)

while True:
    try:
        data, addr = sock.recvfrom(1024)
        if data:
            cmd_id = struct.unpack(">H", data[:2])[0]
            publish.single(Topic, payload=str(cmd_id), hostname=MQTT_BROKER, port=MQTT_PORT)
            logger.info(f"Published CMD {cmd_id} to MQTT")
    except Exception as e:
        logger.error(f"Loop error: {e}")