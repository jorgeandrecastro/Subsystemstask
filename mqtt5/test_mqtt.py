import paho.mqtt.publish as publish

# "localhost" fonctionne si ton broker MQTT est sur Windows
# Sinon utilise "host.docker.internal"
MQTT_HOST = "localhost" 
TOPIC = "satelliteSS/radio"

print("Envoi des messages de test vers COSMOS...")

# Test pour le champ MODE
publish.single(TOPIC, "MODE: OPERATIONAL", hostname=MQTT_HOST)

# Test pour le champ VERSION
publish.single(TOPIC, "Version: 1.2.3-FW", hostname=MQTT_HOST)

# Test pour le champ BEACON (message long)
publish.single(TOPIC, "Beacon: Status OK - Voltage: 3.7V - RSSI: -85dBm", hostname=MQTT_HOST)

print("Messages envoyés ! Regarde ton Telemetry Viewer.")