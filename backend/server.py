import requests
import time
import socket
import json
import os
from dotenv import load_dotenv

load_dotenv()

PHYPHOX_URL = os.getenv("PHYPHOX_URL") 
UDP_IP = os.getenv("UDP_IP") 
UDP_PORT = int(os.getenv("UDP_PORT"))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def stream_sensor_data():
    print("Streaming to Blender on port 5005...")
    try:
        while True:
            # Request all 6 buffers
            response = requests.get(f"{PHYPHOX_URL}/get?gyrX&gyrY&gyrZ&linX&linY&linZ", timeout=2)
            data = response.json()

            if 'buffer' in data:
                buf = data['buffer']
                
                # Get the last value of each buffer (defaulting to 0 if empty)
                y = buf.get('gyrX', {}).get('buffer', [0])[-1]
                z = buf.get('gyrY', {}).get('buffer', [0])[-1]
                x = buf.get('gyrZ', {}).get('buffer', [0])[-1]
                
                ay = buf.get('linX', {}).get('buffer', [0])[-1]
                az = buf.get('linY', {}).get('buffer', [0])[-1]
                ax = buf.get('linZ', {}).get('buffer', [0])[-1]
                
                payload = json.dumps({"x": x, "y": y, "z": z, "ax": ax, "ay": ay, "az": az}).encode('utf-8')
                sock.sendto(payload, (UDP_IP, UDP_PORT))
                
                print(payload)
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("Stopped.")

if __name__ == "__main__":
    stream_sensor_data()
    
stream_sensor_data()