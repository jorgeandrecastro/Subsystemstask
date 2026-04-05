from openc3.utilities.logger import Logger
from openc3.api import inject_tlm
import paho.mqtt.client as mqtt
import time

# Configuration
MQTT_BROKER = "host.docker.internal" 
MQTT_PORT = 1883 
TOPIC = "satelliteSS/#"

def on_message(client, userdata, message):
    try:
        msg = message.payload.decode()
        # On filtre pour ne prendre que les messages de l'OBC
        if "ObcSS" in msg:
            Logger.info(f"OBC MQTT reçu : {msg}")
            
            # 1. Firmware -> Paquet GET_VERSION
            if "Firmware" in msg:
                inject_tlm("OBC", "GET_VERSION", {"FW_VER": msg})
                Logger.info(f"Injecté OBC VERSION: {msg}")

            # 2. Uptime / Startup -> Paquet GET_UPTIME
            elif "Startup" in msg or "Connected" in msg:
                inject_tlm("OBC", "GET_UPTIME", {"TIME_VAL": msg})
                Logger.info(f"Injecté OBC UPTIME: {msg}")

            # 3. Le reste (ID value, etc.) -> Paquet SET_DESIGNATOR
            else:
                inject_tlm("OBC", "SET_DESIGNATOR", {"DATA": msg})
                Logger.info(f"Injecté OBC DESIGNATOR: {msg}")

    except Exception as e:
        Logger.error(f"Erreur processing OBC : {e}")

def main():
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    
    while True:
        try:
            Logger.info(f"Connexion OBC MQTT sur {MQTT_BROKER}...")
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            client.subscribe(TOPIC)
            client.loop_forever()
        except Exception as e:
            Logger.error(f"Échec OBC : {e}. Retrying in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    main()