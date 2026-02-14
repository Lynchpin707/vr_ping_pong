import bge
import socket
import json
import select

cont = bge.logic.getCurrentController()
racket = cont.owner
keyboard = bge.logic.keyboard

# --- NETWORK SETUP (For Rotation) ---
if 'udp' not in bge.logic.globalDict:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 5005))
    sock.setblocking(False)
    bge.logic.globalDict['udp'] = sock

sock = bge.logic.globalDict['udp']
ready = select.select([sock], [], [], 0.0)

# 1. APPLY ROTATION FROM PHONE
if ready[0]:
    try:
        data, _ = sock.recvfrom(1024)
        sensor = json.loads(data.decode('utf-8'))
        
        rx, ry, rz = sensor.get('x', 0), sensor.get('y', 0), sensor.get('z', 0)
        racket.applyRotation([rx * 0.05, ry * 0.05, rz * 0.05], True)
    except Exception:
        pass

# 2. APPLY MOVEMENT FROM KEYBOARD
move_speed = 0.2
pos = racket.worldPosition

# Left / Right (Y-Axis)
if keyboard.events[bge.events.AKEY] == bge.logic.KX_INPUT_ACTIVE or keyboard.events[bge.events.QKEY] == bge.logic.KX_INPUT_ACTIVE or keyboard.events[bge.events.LEFTARROWKEY] == bge.logic.KX_INPUT_ACTIVE:
    pos.y -= move_speed
if keyboard.events[bge.events.DKEY] == bge.logic.KX_INPUT_ACTIVE or keyboard.events[bge.events.RIGHTARROWKEY] == bge.logic.KX_INPUT_ACTIVE:
    pos.y += move_speed

# Forward / Backward (X-Axis)
if keyboard.events[bge.events.ZKEY] == bge.logic.KX_INPUT_ACTIVE or keyboard.events[bge.events.UPARROWKEY] == bge.logic.KX_INPUT_ACTIVE:
    pos.x -= move_speed
if keyboard.events[bge.events.SKEY] == bge.logic.KX_INPUT_ACTIVE or keyboard.events[bge.events.DOWNARROWKEY] == bge.logic.KX_INPUT_ACTIVE:
    pos.x += move_speed

# 3. CLAMP LIMITS & LOCK HEIGHT
pos.y = max(-4.0, min(4.0, pos.y)) # Left/Right boundaries
pos.x = max(-6.0, min(0.0, pos.x)) # Forward/Backward boundaries (Adjust these to fit your table)
pos.z = 1.0  # Lock Height (Z-Axis)

racket.worldPosition = pos