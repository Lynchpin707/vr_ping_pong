import bge
import socket
import json
import select

cont = bge.logic.getCurrentController()
racket = cont.owner

if 'config' not in bge.logic.globalDict:
    config_path = bge.logic.expandPath('//config.json')
    with open(config_path, 'r') as f:
        bge.logic.globalDict['config'] = json.load(f)

cfg = bge.logic.globalDict['config']


if 'udp' not in bge.logic.globalDict:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((cfg['network']['host'], cfg['network']['port']))
    sock.setblocking(False)
    bge.logic.globalDict['udp'] = sock
    bge.logic.globalDict['vx'] = 0.0
    bge.logic.globalDict['vy'] = 0.0

sock = bge.logic.globalDict['udp']
ready = select.select([sock], [], [], 0.0)

pos = racket.worldPosition.copy() 
move_speed = cfg['physics']['move_speed']
friction = cfg['physics']['friction']
deadzone = cfg['physics']['deadzone']

if ready[0]:
    try:
        data, _ = sock.recvfrom(1024)
        sensor = json.loads(data.decode('utf-8'))
        
        rx, ry, rz = sensor.get('x', 0), sensor.get('y', 0), sensor.get('z', 0)
        racket.applyRotation([rx * 0.05, ry * 0.05, rz * 0.05], True)
        
        ax = sensor.get('ax', 0)
        ay = sensor.get('ay', 0)
        
        if abs(ax) < deadzone: ax = 0
        if abs(ay) < deadzone: ay = 0
        
        bge.logic.globalDict['vx'] += ax * move_speed
        bge.logic.globalDict['vy'] += -ay * move_speed

    except Exception:
        pass

bge.logic.globalDict['vx'] *= friction
bge.logic.globalDict['vy'] *= friction

pos.x += bge.logic.globalDict['vx']
pos.y += bge.logic.globalDict['vy']

x_min, x_max = cfg['limits']['x_min'], cfg['limits']['x_max']
y_min, y_max = cfg['limits']['y_min'], cfg['limits']['y_max']

if pos.y > y_max or pos.y < y_min:
    bge.logic.globalDict['vy'] = 0.0
pos.y = max(y_min, min(y_max, pos.y))

if pos.x > x_max or pos.x < x_min:
    bge.logic.globalDict['vx'] = 0.0
pos.x = max(x_min, min(x_max, pos.x))

pos.z = cfg['limits']['z_lock']

racket.worldPosition = pos