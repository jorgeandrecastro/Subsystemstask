import time
import sys
import socket
import struct
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import paho.mqtt.client as mqtt
    import paho.mqtt.publish as publish
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paho-mqtt==1.6.1"])
    import paho.mqtt.client as mqtt
    import paho.mqtt.publish as publish

# Configuration OBC (ports différents de COMMS)
port = 8090  # DIFFERENT de 8080 (COMMS)
host = "0.0.0.0"
Topic = "satelliteSS/obc"  # DIFFERENT de satelliteSS/radio
MQTTBROKER = "192.168.1.84"

# Commandes OBC uniquement (Table 2)
CMD_MAP = {
    0x0200: "OBC_SET_DESIGNATOR_0",
    0x0201: "OBC_SET_DESIGNATOR_1",
    0x0202: "OBC_SET_DESIGNATOR_2",
    0x0203: "OBC_SET_DESIGNATOR_3",
    0x0204: "OBC_SET_HK_PERIOD_516",
    0x0205: "OBC_SET_HK_PERIOD_517",
    0x0206: "OBC_SET_HK_PERIOD_518",
    0x0207: "OBC_SET_HK_PERIOD_519",
    0x0208: "OBC_SET_HK_PERIOD_520",
    0x0209: "OBC_SET_HK_PERIOD_521",
    0x020A: "OBC_SET_HK_PERIOD_522",
    0x020B: "OBC_SET_HK_PERIOD_523",
    0x020C: "OBC_SET_HK_PERIOD_524",
    0x020D: "OBC_SET_HK_PERIOD_525",
    0x020E: "OBC_SET_HK_PERIOD_526",
    0x020F: "OBC_GET_VERSION",
    0x0210: "OBC_GET_IMAGE",
    0x0211: "OBC_GET_UPTIME",
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))
logger.info(f"OBC PacketHandler listening on {host}:{port}")

while True:
    try:
        sock.settimeout(10)
        data, addr = sock.recvfrom(1024)
        
        if data:
            logger.info(f"OBC Received: {data.hex()} from {addr}")
            
            if len(data) >= 2:
                cmd = struct.unpack(">H", data[:2])[0]
                logger.info(f"OBC Command ID: {cmd} ({hex(cmd)})")

                if cmd in CMD_MAP:
                    cmd_name = CMD_MAP[cmd]
                    logger.info(f"OBC VALID: {cmd_name} -> MQTT")
                    publish.single(Topic, payload=str(cmd), hostname=MQTTBROKER)
                else:
                    logger.warning(f"OBC Invalid: {hex(cmd)}")

    except socket.timeout:
        pass
    except Exception as err:
        logger.error(f"OBC Error: {err}")
        time.sleep(1)