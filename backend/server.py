import requests
import time
import socket
import json
import os
from dotenv import load_dotenv

load_dotenv()

PHYPHOX_URL = os.getenv("PHYPHOX_URL") 
UDP_IP = os.getenv("UDP_IP") 
UDP_PORT = int(os.getenv("UDP_PORT") )

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def stream_sensor_data():
    requests.get(f"{PHYPHOX_URL}/control?cmd=start")
    print("Streaming to Blender on port 5005...")
    
    try:
        while True:
            response = requests.get(f"{PHYPHOX_URL}/get?gyrX&gyrY&gyrZ", timeout=2)
            data = response.json()

            print("RAW DATA:", data) 
            
            if 'buffer' in data:
                x_list = data['buffer'].get('gyrX', {}).get('buffer', [0])
                y_list = data['buffer'].get('gyrY', {}).get('buffer', [0])
                z_list = data['buffer'].get('gyrZ', {}).get('buffer', [0])
                
                x = x_list[-1] if x_list else 0
                y = y_list[-1] if y_list else 0
                z = z_list[-1] if z_list else 0
                
                print(f"Rotation -> X: {x:.2f} | Y: {y:.2f} | Z: {z:.2f}")
                
                payload = json.dumps({"x": x, "y": y, "z": z}).encode('utf-8')
                sock.sendto(payload, (UDP_IP, UDP_PORT))
            else:
                print("Warning: 'buffer' key not found in the response.")
                
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        requests.get(f"{PHYPHOX_URL}/control?cmd=stop")

if __name__ == "__main__":
    stream_sensor_data()

stream_sensor_data()