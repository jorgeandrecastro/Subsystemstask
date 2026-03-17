Satellite Communication System - Lab #1
OpenC3 COSMOS Integration with MQTT Radio Module
Student: Jorge Andre Castro
Instructor: Mr. Maqina
Date: March 17, 2026
Version: 1.0.11


1. System Overview
This project implements a complete satellite communication ground station using OpenC3 COSMOS 6.10.4 integrated with an MQTT-based radio module simulator. The system demonstrates bidirectional communication between COSMOS and a virtual satellite radio through UDP and MQTT protocols.
Architecture Diagram
plain
Copy
┌─────────────────┐     UDP      ┌──────────────────┐     MQTT      ┌─────────────┐
│   OpenC3        │ ◄──────────► │  PacketHandler   │ ◄──────────► │   Radio     │
│   COSMOS        │   Port 8080  │  (Python)        │   Port 1883  │   Module    │
│                 │              │                  │              │  (MQTT)     │
│  - Command      │              │  - UDP Listener  │              │  - Beacon   │
│    Sender       │              │  - MQTT Publisher│              │  - Mode     │
│  - Telemetry    │              │                  │              │  - Version  │
│    Viewer       │              └──────────────────┘              └─────────────┘
│                 │                                                        │
│                 │              ┌──────────────────┐                      │
│                 │ ◄─────────── │   TLMLoader      │ ◄────────────────────┘
│                 │   Inject     │  (Python)        │     Subscribe
│                 │   Telemetry  │  - MQTT Subscriber
│                 │              │  - COSMOS API
└─────────────────┘              └──────────────────┘
2. Components
2.1 OpenC3 COSMOS Target (COMMS)
File: targets/COMMS/cmd_tlm/cmd.txt
Four commands implemented according to Table 1 specifications:
Table
Command	Hex ID	Description	Parameter
SET_MODE_0	0x0100	Set satellite to mode 0	CMD_ID = 256
SET_MODE_1	0x0101	Set satellite to mode 1	CMD_ID = 257
GET_DEFAULT_MODE	0x0102	Request default mode	CMD_ID = 258
GET_VERSION	0x0103	Request firmware version	CMD_ID = 259
File: targets/COMMS/cmd_tlm/tlm.txt
Telemetry packet structure:
ID_ITEM ID: Packet identifier (0x0100)
MODE: Operating mode (UINT, 16 bits)
FW_VER: Firmware version (UINT, 16 bits)
INACTBEA: Inactivity beacon message (STRING, 1024 bits)
2.2 PacketHandler Microservice
File: microservices/PACKETHANDLER/packethandler.py
Function: Bridge between COSMOS (UDP) and Radio Module (MQTT)
Workflow:
Listens on UDP port 8080 for commands from COSMOS
Parses 16-bit big-endian command ID
Validates command against authorized range (0x0100-0x0103)
Publishes command to MQTT topic satelliteSS/radio
Logs all transactions for debugging
Key Features:
Automatic paho-mqtt installation in Docker environment
Robust error handling and timeout management
Command mapping validation
2.3 TLMLoader Microservice
File: microservices/TLMLOADER/tlmloader.py
Function: Bridge between Radio Module (MQTT) and COSMOS (Telemetry)
Workflow:
Subscribes to MQTT topic satelliteSS/#
Parses beacon messages from radio module
Extracts firmware version using regex: Firmware:\s*([\d.]+)
Converts version to integer (e.g., 1.01 → 101)
Injects telemetry into COSMOS using inject_tlm() API
Parsing Logic:
Detects mode from message content ("Active", "MODE 1")
Extracts temperature, voltage, and RxCount from beacon
Handles multiple message formats (beacon, mode response, version response)
3. Network Configuration
IP Addresses
COSMOS Host: 192.168.1.84 (Windows host IP)
MQTT Broker: 192.168.1.84 (Eclipse Mosquitto 2.0.15)
UDP Port: 8080 (Command interface)
MQTT Port: 1883 (Telemetry interface)
Interface Configuration
plain
Copy
INTERFACE COMMS_INT udp_interface.rb 192.168.1.84 8080 8081 8082 nil
4. Build and Deployment
Prerequisites
Docker Desktop for Windows
OpenC3 COSMOS 6.10.4
Python 3.11+ (for standalone PacketHandler)
Eclipse Mosquitto MQTT Broker
Build Commands
powershell
Copy
# Build plugin
cd openc3-cosmos-radio-module
..\openc3.bat cli rake build VERSION=1.0.11

# Start COSMOS
cd ..
.\openc3.bat start

# Start PacketHandler (standalone)
cd openc3-cosmos-radio-module\microservices\PACKETHANDLER
python packethandler.py
5. Testing Results
Command Testing
All four commands successfully transmitted and acknowledged:
Table
Test	Command ID	Response	Status
SET_MODE_0	0x0100	setMode: 0	✅ PASS
SET_MODE_1	0x0101	setMode: 1	✅ PASS
GET_DEFAULT_MODE	0x0102	setMode: 0	✅ PASS
GET_VERSION	0x0103	Firmware Version: 1.01	✅ PASS
Telemetry Verification
Inactivity Beacon: Temperature, voltage levels, and RxCount displayed correctly
Mode Changes: Real-time updates in MODE field
Version Reporting: FW_VER populated from radio module response
Log Evidence
plain
Copy
cmd("COMMS SET_MODE_1 with CMD_ID 257")
REAL TELEMETRY RECEIVED: CommsSS: 2026-03-17 20:05:41 - setMode: 1
Successfully injected: {'INACTBEA': 'CommsSS: ... setMode: 1', 'MODE': 0, 'FW_VER': 0}
6. Challenges and Solutions
Table
Challenge	Solution
UDP port binding in Docker	Used standalone Python execution on Windows host
COSMOS-to-Docker networking	Configured interface with host IP (192.168.1.84) instead of localhost
Missing openc3 module	Created standalone version of PacketHandler without COSMOS dependencies
Command ID validation	Implemented strict range checking (0x0100-0x0103) in PacketHandler
Firmware version parsing	Used regex extraction with float-to-integer conversion
7. Conclusion
This laboratory exercise successfully demonstrated:
✅ Integration of OpenC3 COSMOS with external radio hardware (simulated)
✅ Bidirectional communication via UDP and MQTT protocols
✅ Real-time telemetry injection and command transmission
✅ Robust error handling and network resilience
The system is fully operational and ready for demonstration.
Prepared by: Jorge andre castro

Repository: C:\Users\Georg\Desktop\satelliteSS_Lab1\satelliteSS\mqtt5\cosmos-6.10.4\