Satellite OBC Module - Lab #2
OpenC3 COSMOS Integration with Onboard Computer
Student: Jorge andre Castro
Course: Satellite Communication Systems
Institution: Cape Peninsula University of Technology / F'SATI
1. Overview
This project implements an independent Onboard Computer (OBC) ground station interface using OpenC3 COSMOS 6.10.4. The system communicates with a virtual satellite OBC via UDP and MQTT protocols, providing real-time command and telemetry capabilities for satellite housekeeping operations.
2. System Architecture
plain
Copy
┌─────────────┐    UDP     ┌─────────────┐    MQTT    ┌─────────┐
│   COSMOS    │ ◄────────► │  Packet     │ ◄────────► │  OBC    │
│   (OBC      │   Port     │  Handler    │   Topic    │  App    │
│   Target)   │   8090     │  (Python)   │  satelliteSS/obc  │  (Sim)  │
└─────────────┘            └─────────────┘            └─────────┘
       ▲                                                       │
       │                                                       │
       └───────────────────────────────────────────────────────┘
                         MQTT Telemetry
                    (TLMLoader injects to COSMOS)
3. Command Set (Table 2)
Table
Command	Hex Range	Decimal	Function
SET_DESIGNATOR	0x0200-0x0203	512-515	Assign OBC ID (0-3)
SET_HK_BEACON_PERIOD	0x0204-0x020E	516-526	Set housekeeping interval
GET_VERSION	0x020F	527	Request firmware version
GET_IMAGE	0x0210	528	Request boot images
GET_UPTIME	0x0211	529	Request startup time
4. Telemetry Structure
Table
Field	Type	Description
OBC_ID	UINT 8	Designator (0-3)
UPTIME	UINT 32	Seconds since startup
FW_VERSION	UINT 16	Firmware (x100)
BOOT_IMAGE	UINT 8	Current image
NEXT_IMAGE	UINT 8	Next boot image
HK_PERIOD	UINT 16	Beacon interval
TEMP	UINT 16	Temperature (x100)
VOLTAGE_3V	UINT 16	3.3V rail (x100)
VOLTAGE_5V	UINT 16	5V rail (x100)
HK_MESSAGE	STRING	Raw housekeeping data
5. File Structure
plain
Copy
openc3-cosmos-obc-module/
├── targets/OBC/cmd_tlm/
│   ├── cmd.txt          # 5 command definitions
│   └── tlm.txt          # Telemetry packet structure
├── microservices/
│   ├── PACKETHANDLER/
│   │   └── packethandler.py    # UDP to MQTT bridge
│   └── TLMLOADER/
│       └── tlmloader.py        # MQTT to COSMOS injector
├── plugin.txt           # Interface configuration
└── openc3-cosmos-obc-module.gemspec
6. Network Configuration
Table
Parameter	Value
COSMOS Host	192.168.1.84
UDP Command Port	8090
MQTT Broker	192.168.1.84:1883
MQTT Topic	satelliteSS/obc
7. Build & Run
Build Plugin
powershell
Copy
cd openc3-cosmos-obc-module
..\openc3.bat cli rake build VERSION=1.0.0
Start COSMOS
powershell
Copy
cd ..
.\openc3.bat start
Run OBC Simulator
powershell
Copy
.\ObcApp.exe 192.168.1.84
Run Packet Handler (standalone)
powershell
Copy
cd openc3-cosmos-obc-module\microservices\PACKETHANDLER
python packethandler.py
8. Test Results
All 5 commands validated and operational:
plain
Copy
✅ SET_DESIGNATOR (0x200)      → OBC ID assignment
✅ SET_HK_BEACON_PERIOD (0x208) → 520s interval set
✅ GET_VERSION (0x20F)          → Firmware 1.01
✅ GET_IMAGE (0x210)            → Boot images retrieved
✅ GET_UPTIME (0x211)           → Startup time received
9. Key Features
Independent Module: Separate from Lab #1 COMMS system
Bidirectional Communication: Commands and telemetry
Real-time Processing: UDP → MQTT → COSMOS pipeline
Robust Parsing: Regex-based telemetry extraction
Standalone Execution: PacketHandler runs outside Docker
10. Technologies
OpenC3 COSMOS 6.10.4
Python 3.11
MQTT (paho-mqtt 1.6.1)
UDP Sockets
Docker Desktop
Repository: https://github.com/jorgeandrecastro/satelliteSS-cosmos-obc
Date: March 17, 2026