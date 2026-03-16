import bge
import socket
import json
import select

cont = bge.logic.getCurrentController()
racket = cont.owner


if 'udp' not in bge.logic.globalDict:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 5005))
    sock.setblocking(False)
    bge.logic.globalDict['udp'] = sock
    bge.logic.globalDict['vx'] = 0.0
    bge.logic.globalDict['vy'] = 0.0

sock = bge.logic.globalDict['udp']
ready = select.select([sock], [], [], 0.0)

pos = racket.worldPosition.copy() 
move_speed = 0.15  
friction = 0.7    
deadzone = 0.15     

if ready[0]:
    try:
        data, _ = sock.recvfrom(1024)
        sensor = json.loads(data.decode('utf-8'))
        
        rx, ry, rz = sensor.get('x', 0), sensor.get('y', 0), sensor.get('z', 0)
        racket.applyRotation([rx * 0.05, ry * 0.05, rz * 0.05], True)

        # 2. MOVEMENT (Acceleration -> Velocity)
        ax = sensor.get('ax', 0)
        ay = sensor.get('ay', 0)
        
        # Apply deadzone
        if abs(ax) < deadzone: ax = 0
        if abs(ay) < deadzone: ay = 0
        
        # Accumulate velocity
        bge.logic.globalDict['vx'] += ax * move_speed
        bge.logic.globalDict['vy'] += -ay * move_speed

    except Exception:
        pass

# Apply friction to gradually stop the racket
bge.logic.globalDict['vx'] *= friction
bge.logic.globalDict['vy'] *= friction

# Apply velocity to position
pos.x += bge.logic.globalDict['vx']
pos.y += bge.logic.globalDict['vy']

# 3. CLAMP LIMITS & KILL VELOCITY ON IMPACT
if pos.y > 2.0 or pos.y < -2.0:
    bge.logic.globalDict['vy'] = 0.0
pos.y = max(-2.0, min(2.0, pos.y))

if pos.x > 0.0 or pos.x < -2.0:
    bge.logic.globalDict['vx'] = 0.0
pos.x = max(-2.0, min(2.0, pos.x))

pos.z = 1.0  

racket.worldPosition = pos

