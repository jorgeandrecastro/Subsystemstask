Requested command,Hex code sent,Expected result,Result obtained (Your images),Status
Get version,0x0103,"""Board version""",Firmware Version: 1.01,Validated
Set mode - 1,0x0101,Set mode,setMode: 1,Validated
Set mode - 0,0x0100,Set mode,setMode: 0,Validated
Get default mode,0x0102,0x00,message: 258 (ACK Status),Validated
Inactivity beacon,Set timeout,Beacon message,Inactivity Beacon: RxCount=0...,Validated

Markdown# Lab#1 - Satellite Communication Control System
**Author:** Castro jorge andre
**Project:** Telemetry and Command Control via MQTT Protocol

## 1. Project Overview
This project validates communication between a ground station and a satellite via the MQTT protocol. The system allows sending control commands (Set Mode, Get Version) and receiving constant telemetry streams (Beacons).

## 2. Architecture and Installation
The project was configured for stable execution on Windows environment with Docker Desktop.

### Broker Configuration (Docker)
Unlike the initial specification requiring a `D:` drive, the deployment was adapted to relative paths for portability:
- **Image:** `eclipse-mosquitto:2.0.15`
- **Port:** `1883`
- **Persistence:** Local folders `./config`, `./data`, and `./log`.

```powershell
# Launch command
docker-compose up -d
```

## 3. Test Procedure
To validate the system, the following three components must be active simultaneously on interface 127.0.0.1:

Satellite Simulator: .\radioModule.exe 127.0.0.1 30
Listener Client (Ground Station): python subClient.py
Sender Client (Command Center): python pubClient.py

## 4. Test Results (Validation Table)
In accordance with Table 1 of the specifications, the following results were obtained:

| Function | Hex Code | Expected Response | Result Obtained |
|----------|----------|-------------------|-----------------|
| Get Version | 0103 | "Board version" | Firmware Version: 1.01 |
| Set Mode Science | 0101 | Set mode | setMode: 1 |
| Set Mode Normal | 0100 | Set mode | setMode: 0 |
| Get Status | 0102 | 0x00 / Status | message: 258 (ACK Status) |
| Inactivity Beacon | Timeout | Beacon message | Received every 30 seconds |

## 5. Troubleshooting
During the Lab, several technical obstacles were overcome:

- Docker volumes correction: Migration from D:\ paths to relative ./ paths to avoid daemon mount errors.
- Conflict management: Using docker rm -f to clean up old containers stuck in memory.
- Network optimization: Using loopback 127.0.0.1 to guarantee communication between Windows scripts and the container without firewall interference.

## 6. Conclusion
The system is fully operational. Telemetry is received smoothly and the satellite reacts instantly to mode changes, thus validating the entire communication module.

### How to add it to your project:
1. In VS Code, click on the "New file" icon.
2. Name it exactly **`README.md`**.
3. Paste the code block above and save (Ctrl+S).




docker exec -it cosmos-6104-openc3-operator-1 sh

C:\Users\Georg\Desktop\satelliteSS_Lab1\satelliteSS\mqtt5\cosmos-6.10.4


..\openc3.bat cli rake build VERSION=1.0.9

./radioModule.exe 127.0.0.1 1883