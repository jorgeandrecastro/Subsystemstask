import time
import sys
import socket
import struct
import logging

# Configuration du logging (remplace Logger de COSMOS)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Installation de paho-mqtt
try:
    import paho.mqtt.client as mqtt
    import paho.mqtt.publish as publish
except ImportError:
    logger.info("Installing paho-mqtt...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paho-mqtt==1.6.1"])
    import paho.mqtt.client as mqtt
    import paho.mqtt.publish as publish

# Configuration réseau
port = 8080
host = "0.0.0.0"
Topic = "satelliteSS/radio"
MQTTBROKER = "192.168.1.84"

# Mapping des commandes selon Tableau 1
CMD_MAP = {
    0x0100: "SET_MODE_0",
    0x0101: "SET_MODE_1",
    0x0102: "GET_DEFAULT_MODE",
    0x0103: "GET_VERSION"
}

# Initialisation du Socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))
logger.info(f"Listening for UDP packets on {host}:{port}")

while True:
    try:
        sock.settimeout(10)
        data, addr = sock.recvfrom(1024)
        
        if data:
            logger.info(f"Received raw data: {data.hex()} from {addr}")
            
            if len(data) >= 2:
                # Extraction ID commande (Big-Endian)
                cmd = struct.unpack(">H", data[:2])[0]
                logger.info(f"Detected Command ID: {cmd} (Hex: {hex(cmd)})")

                # Vérification plage autorisée (Tableau 1)
                if cmd in CMD_MAP:
                    cmd_name = CMD_MAP[cmd]
                    logger.info(f"VALID COMMAND: {cmd_name} - Publishing to MQTT")
                    publish.single(Topic, payload=str(cmd), hostname=MQTTBROKER)
                else:
                    logger.warning(f"Command {hex(cmd)} is outside authorized range (0x0100-0x0103)")
            else:
                logger.warning(f"Packet too short ({len(data)} bytes)")

    except socket.timeout:
        pass
    except Exception as err:
        logger.error(f"Error in PacketHandler: {err}")
        time.sleep(1)