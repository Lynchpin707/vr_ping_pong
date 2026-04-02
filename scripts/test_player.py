import bge

cont = bge.logic.getCurrentController()
racket = cont.owner
keyboard = bge.logic.keyboard

move_speed = 8.0 # Adjust for harder/softer hits

vx, vy = 0.0, 0.0

# Forward/Backward (X-axis)
if keyboard.events[bge.events.UPARROWKEY] == bge.logic.KX_INPUT_ACTIVE:
    vx = move_speed
if keyboard.events[bge.events.DOWNARROWKEY] == bge.logic.KX_INPUT_ACTIVE:
    vx = -move_speed

# Left/Right (Y-axis)
if keyboard.events[bge.events.LEFTARROWKEY] == bge.logic.KX_INPUT_ACTIVE:
    vy = -move_speed
if keyboard.events[bge.events.RIGHTARROWKEY] == bge.logic.KX_INPUT_ACTIVE:
    vy = move_speed

# Apply velocity for physics impacts
racket.setLinearVelocity([vx, vy, 0.0], False)

# Keep racket on the player's side of the table
pos = racket.worldPosition
pos.x = max(-6.0, min(0.0, pos.x))
pos.y = max(-4.0, min(4.0, pos.y))
pos.z = 1.0
racket.worldPosition = pos