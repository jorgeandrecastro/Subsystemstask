import time
import sys
import socket
import struct
import logging
import paho.mqtt.publish as publish

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# CHANGEMENT ICI : Port 8090 pour l'OBC
UDP_PORT = 8090 
host = "0.0.0.0"
MQTT_BROKER = "host.docker.internal"
MQTT_PORT = 1883
Topic = "satelliteSS/obc" # Topic spécifique OBC

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    sock.bind((host, UDP_PORT))
    logger.info(f"OBC PacketHandler listening on UDP {UDP_PORT}")
except Exception as e:
    logger.error(f"Could not bind OBC: {e}")
    sys.exit(1)

while True:
    try:
        data, addr = sock.recvfrom(1024)
        if data:
            # On récupère l'ID de la commande (ex: 512 pour Set Designator)
            cmd_id = struct.unpack(">H", data[:2])[0]
            publish.single(Topic, payload=str(cmd_id), hostname=MQTT_BROKER, port=MQTT_PORT)
            logger.info(f"OBC Published CMD {cmd_id} to MQTT")
    except Exception as e:
        logger.error(f"OBC Loop error: {e}")