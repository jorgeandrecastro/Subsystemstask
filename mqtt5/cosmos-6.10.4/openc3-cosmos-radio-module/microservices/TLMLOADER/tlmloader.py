from openc3.utilities.logger import Logger
from openc3.api import inject_tlm
import paho.mqtt.client as mqtt
import re
import time

# Configuration
MQTT_BROKER = "host.docker.internal" 
MQTT_PORT = 1883 
TOPIC = "satelliteSS/#"

def on_message(client, userdata, message):
    try:
        msg = message.payload.decode()
        if "CommsSS" in msg:
            Logger.info(f"MQTT reçu : {msg}")
            
            # 1. Cas du message Firmware Version -> Paquet VERSION
            if "Firmware Version" in msg:
                # On injecte dans le paquet VERSION, item FW_VER
                inject_tlm("COMMS", "VERSION", {"FW_VER": msg})
                Logger.info(f"Injecté dans VERSION: {msg}")

            # 2. Cas du message setMode -> Paquet SET_MODE
            elif "setMode" in msg:
                # On injecte dans le paquet SET_MODE, item MODE
                inject_tlm("COMMS", "SET_MODE", {"MODE": msg})
                Logger.info(f"Injecté dans SET_MODE: {msg}")

            # 3. Tout le reste (Beacons, etc.) -> Paquet BEACON
            else:
                # On injecte dans le paquet BEACON, item INACTBEA
                inject_tlm("COMMS", "BEACON", {"INACTBEA": msg})
                Logger.info(f"Injecté dans BEACON: {msg}")

    except Exception as e:
        Logger.error(f"Erreur de processing : {e}")

def main():
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    
    while True:
        try:
            Logger.info(f"Connexion MQTT sur {MQTT_BROKER}...")
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            client.subscribe(TOPIC)
            client.loop_forever()
        except Exception as e:
            Logger.error(f"Échec connexion : {e}. Retrying in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    main()