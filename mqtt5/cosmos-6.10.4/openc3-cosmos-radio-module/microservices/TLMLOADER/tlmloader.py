from openc3.utilities.logger import Logger
from openc3.api import inject_tlm
import paho.mqtt.client as mqtt
import re

# Utilise ton IP réelle 192.168.1.84
MQTTBROKER = "192.168.1.84" 
TOPIC = "satelliteSS/#"

def on_message(client, userdata, message):
    try:
        msg = message.payload.decode()
        
        # On ne traite que les messages venant de la Radio (ceux qui commencent par CommsSS)
        if "CommsSS" in msg:
            Logger.info(f"REAL TELEMETRY RECEIVED: {msg}")
            
            # INITIALISATION DES DONNÉES
            tlm_data = {
                "INACTBEA": msg,  # Le message complet affiché dans la zone de texte
                "MODE": 0,         # Valeur par défaut
                "FW_VER": 0        # Valeur par défaut
            }

            # EXTRACTION DU FIRMWARE (ex: "Firmware: 1.01" -> 101)
            # On cherche un nombre après le mot "Firmware:"
            fw_match = re.search(r"Firmware:\s*([\d.]+)", msg)
            if fw_match:
                # On multiplie par 100 pour transformer 1.01 en entier 101 (UINT dans tlm.txt)
                tlm_data["FW_VER"] = int(float(fw_match.group(1)) * 100)

            # DETECTION DU MODE (Optionnel selon ce que ta radio renvoie)
            if "Active" in msg or "MODE 1" in msg:
                tlm_data["MODE"] = 1
            else:
                tlm_data["MODE"] = 0

            # INJECTION DANS COSMOS
            # Cible: COMMS, Paquet: STATUS
            inject_tlm("COMMS", "STATUS", tlm_data)
            Logger.info(f"Successfully injected: {tlm_data}")

    except Exception as e:
        Logger.error(f"Error processing telemetry: {e}")

def main():
    # Configuration du client MQTT
    client = mqtt.Client()
    client.on_message = on_message
    
    try:
        Logger.info(f"Connecting to MQTT Broker at {MQTTBROKER}...")
        client.connect(MQTTBROKER, 1883, 60)
        client.subscribe(TOPIC)
        
        Logger.info(f"TLMLoader is running. Subscribed to {TOPIC}")
        client.loop_forever()
    except Exception as e:
        Logger.error(f"Failed to connect to Broker: {e}")

if __name__ == "__main__":
    main()