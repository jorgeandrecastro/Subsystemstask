# OpenC3 Cosmos Radio Module - satelliteSS

## Purpose
OpenC3 plugin to integrate the **radio module** via **MQTT** (Mosquitto). Bidirectional bridge:

- **Commandes UDP** → MQTT `satelliteSS/radio`
- **MQTT** `satelliteSS/#` → TLM OpenC3 (target **COMMS**)

## Key Ports
| Service | Protocole | Port | Host              |
|---------|-----------|------|-------------------|
| PACKETHANDLER | UDP  | 8080 | localhost         |
| MQTT    | TCP   | 1883 | host.docker.internal |

## Features
### 1. PACKETHANDLER (UDP → MQTT)
- Listens on UDP 8080
- Extracts command ID (2 bytes big-endian)
- Publishes to MQTT `satelliteSS/radio`

**Exemple:**
```python
cmd_id = struct.unpack('>H', data[:2])[0]  # ex: 258 pour SET_MODE
publish.single('satelliteSS/radio', str(cmd_id), ...)
```

### 2. TLMLOADER (MQTT → OpenC3 TLM)
- Subscribes to `satelliteSS/#`
- Parses and injects TLM:

| Message Type     | Example              | TLM Packet  | Item    |
|------------------|----------------------|-------------|---------|
| Firmware Version | Firmware v1.2       | VERSION     | FW_VER  |
| setMode          | setMode OPERATIONAL | SET_MODE    | MODE    |
| Beacon/Other     | Beacon data         | BEACON      | INACTBEA|

## Main Commands
| Nom      | ID  | Packet             |
|----------|-----|--------------------|
| SET_MODE | 258 | SET_MODE BIG_ENDIAN|
| VERSION  | 259 | VERSION BIG_ENDIAN |

**TLM:** All items STRING (1024 bits)

## Installation & Startup
1. **Build:** `rake build VERSION=1.0.9`
2. **OpenC3 Admin → Plugins → Install** `openc3-cosmos-radio-module-1.0.9.gem`
3. **Start services:**
   ```
   docker compose -f mqtt5/compose.yml up
   ```
4. Check PACKETHANDLER/TLMLOADER microservices active.

## Proof of Functionality
Screenshots:
- `Photos test/radio0100.png`: TLM displayed
- `Photos test/commande0101.png`: Command sent
- `PhotosTestmosquittoCosmo/`: MQTT→Cosmos tests

**Troubleshooting:**
- Check MQTT broker (mosquitto.conf, docker logs)
- Microservice logs: `docker logs <container>`
- Free ports: 8080 UDP, 1883 TCP

**Dependencies:** `paho-mqtt` (auto via requirements.txt)

---

*satelliteSS Lab1 Plugin - Radio Module MQTT-OpenC3 Bridge*
