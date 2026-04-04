# Invincible : Virtual Reality Ping Pong game
You want to play ping-pong but you don't have a table at your disposition ? Forget expensive VR headsets. What if your phone was the racket?

<div align="center">
	<img width="170" src="docs/logo.jpeg" alt="Hadoop">
</div>


Invincible is an immersive 3D ping-pong game that turns your smartphone into a motion-based controller. Built as an academic project at ENSIAS, this game combines real-time sensor telemetry, 3D physics simulation, and a predictive AI opponent into a seamless, accessible VR experience.

## Features
- **Smartphone-as-a-Racket:** Uses the gyroscope and accelerometer in your phone to track swings in real-time.

- **Smart AI Opponent:** A built-in AI that calculates ball trajectories and intercepts your shots using kinematic equations.

- **Zero-Code Tuning:** Adjust the "game feel" (speed, friction, deadzones) instantly via a simple config.json file.


## High-level Architecture 
![High Level Architecture](docs/diagrams/Architecture.drawio.png)
We kept our system architecture simple. The smartphone acts as the physical controller, using the Phyphox app to capture inertial sensor data. A Python-based backend server intercepts this telemetry, processes the raw values, and forwards them via a low-latency UDP connection. Finally, the UPBGE game engine consumes this data stream to update the virtual racket's spatial coordinates, calculate physical collisions, and drive the predictive AI opponent.

### The Tech Stack
- UPBGE: The core game engine (built on Blender). We chose it because it natively runs Python for game logic!

- Blender: For modeling the 3D assets, textures, and environment.

- Python: The brain of the operation. Handles network routing, data cleaning, and the AI controller.

- Phyphox: An awesome mobile app that captures raw sensor data and streams it over HTTP.


## Prerequisites
- A laptop with UPBGE installed.
- Python 3.x
- A smartphone with the Phyphox app installed.
- 15+ years of ping-pong playing experience. (kidding... mostly)

## Installation
1. Clone the repo:

```bash
git clone https://github.com/Lynchpin707/vr_ping_pong.git
cd vr_ping_pong
```
2. Install the Python dependencies:
```bash
pip install -r requirements.txt
```
3. Set up your .env file with your phone's Phyphox IP:
```
PHYPHOX_URL=http://<YOUR_PHYPHOX_GIVEN_IP@>:8080
UDP_IP=127.0.0.1
UDP_PORT=5005
```

4. Start the remote access server on the Phyphox app. and run the data server:

```bash
python scripts/server.py
```
5. Open main.blend in UPBGE and press P. Et voila! You are one step into becoming invincible in PingPong. Have fun !

### -> Tuning the Game Feel
Want to make the racket more sensitive or change the table boundaries? 

Just edit config.json:

```json
{
  "physics": {
    "move_speed": 0.15,
    "friction": 0.7,
    "deadzone": 0.10
  }
}
```
For example : if your racket is jittery -> increase the deadzone .

## The team behind "Invincible"

We are 4 Data engineering students @Ensias. We like PingPong, we like Invincible (yes, the show) and we needed a killer project for our 3D modeling course. So we made *"Invincible : A Virtual Reality Ping Pong game"*.

If you are ready to become INVINCIBLE in PingPong, give it a try and let us know !