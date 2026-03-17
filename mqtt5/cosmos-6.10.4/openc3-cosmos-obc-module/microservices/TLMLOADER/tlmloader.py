from openc3.utilities.logger import Logger
from openc3.api import inject_tlm
import paho.mqtt.client as mqtt
import re

MQTTBROKER = "192.168.1.84"
TOPIC = "satelliteSS/obc"  # Topic OBC uniquement

def on_message(client, userdata, message):
    try:
        msg = message.payload.decode()
        
        # OBC uniquement
        if "ObcSS" in msg:
            Logger.info(f"OBC TELEMETRY: {msg}")
            
            tlm_data = {
                "HK_MESSAGE": msg,
                "OBC_ID": 0,
                "UPTIME": 0,
                "FW_VERSION": 0,
                "BOOT_IMAGE": 0,
                "NEXT_IMAGE": 0,
                "HK_PERIOD": 0,
                "TEMP": 0,
                "VOLTAGE_3V": 0,
                "VOLTAGE_5V": 0
            }
            
            # Extraction OBC_ID (ObcSS0 -> 0)
            obc_match = re.search(r"ObcSS(\d)", msg)
            if obc_match:
                tlm_data["OBC_ID"] = int(obc_match.group(1))
            
            # Extraction Uptime
            uptime_match = re.search(r"Up:\s*(\d+)", msg)
            if uptime_match:
                tlm_data["UPTIME"] = int(uptime_match.group(1))
            
            # Extraction Firmware
            fw_match = re.search(r"Firmware:\s*([\d.]+)", msg)
            if fw_match:
                tlm_data["FW_VERSION"] = int(float(fw_match.group(1)) * 100)
            
            # Extraction Température
            temp_match = re.search(r"Temp:\s*([\d.]+)", msg)
            if temp_match:
                tlm_data["TEMP"] = int(float(temp_match.group(1)) * 100)
            
            # Extraction 3.3V
            v3_match = re.search(r"3V:\s*([\d.]+)", msg)
            if v3_match:
                tlm_data["VOLTAGE_3V"] = int(float(v3_match.group(1)) * 100)
            
            # Extraction 5V
            v5_match = re.search(r"5V:\s*([\d.]+)", msg)
            if v5_match:
                tlm_data["VOLTAGE_5V"] = int(float(v5_match.group(1)) * 100)
            
            inject_tlm("OBC", "STATUS", tlm_data)
            Logger.info(f"OBC injected: {tlm_data}")

    except Exception as e:
        Logger.error(f"OBC Error: {e}")

def main():
    client = mqtt.Client()
    client.on_message = on_message
    
    try:
        Logger.info("OBC TLMLoader starting...")
        client.connect(MQTTBROKER, 1883, 60)
        client.subscribe(TOPIC)
        Logger.info(f"OBC TLMLoader subscribed to {TOPIC}")
        client.loop_forever()
    except Exception as e:
        Logger.error(f"OBC Failed: {e}")

if __name__ == "__main__":
    main()