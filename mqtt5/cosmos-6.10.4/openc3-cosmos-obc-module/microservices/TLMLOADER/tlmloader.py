from openc3.utilities.logger import Logger
from openc3.api import inject_tlm
import paho.mqtt.client as mqtt
import time
import re

MQTT_BROKER = "host.docker.internal"
MQTT_PORT = 1883
TOPIC = "satelliteSS/#"

def parse_hk_beacon(msg):
    """Extrait les champs clé=valeur du message hkBeacon."""
    fields = {}
    # Cherche tous les patterns clé=valeur
    for match in re.finditer(r'(\w+)=([\w.]+)', msg):
        fields[match.group(1)] = match.group(2)
    return fields

def on_message(client, userdata, message):
    try:
        msg = message.payload.decode()

        if "ObcSS" not in msg:
            return

        Logger.info(f"OBC MQTT reçu : {msg}")

        # Toujours injecter le message brut dans SET_DESIGNATOR
        inject_tlm("OBC", "SET_DESIGNATOR", {"DATA": msg})

        if "hkBeacon" in msg:
            fields = parse_hk_beacon(msg)
            Logger.info(f"Champs parsés : {fields}")

            # Injecter upTime dans GET_UPTIME
            if "upTime" in fields:
                inject_tlm("OBC", "GET_UPTIME", {"TIME_VAL": fields["upTime"]})
                Logger.info(f"Injecté UPTIME: {fields['upTime']}")

            # Injecter currentImage ou autre comme version si disponible
            if "currentImage" in fields:
                inject_tlm("OBC", "GET_VERSION", {"FW_VER": f"image_{fields['currentImage']}"})
                Logger.info(f"Injecté VERSION: image_{fields['currentImage']}")

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