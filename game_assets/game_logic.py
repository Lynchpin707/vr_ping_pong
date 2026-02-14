import bge
import socket
import json
import select

cont = bge.logic.getCurrentController()
racket = cont.owner

if 'udp' not in bge.logic.globalDict:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 5005))
    sock.setblocking(False)
    bge.logic.globalDict['udp'] = sock

sock = bge.logic.globalDict['udp']

ready = select.select([sock], [], [], 0.0)

if ready[0]:
    try:
        data, _ = sock.recvfrom(1024)
        rot = json.loads(data.decode('utf-8'))
        racket.applyRotation([rot['x'] * 0.05, rot['y'] * 0.05, rot['z'] * 0.05], True)
        
    except Exception:
        pass