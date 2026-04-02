import bge

cont = bge.logic.getCurrentController()
ball = cont.owner
keyboard = bge.logic.keyboard

if keyboard.events[bge.events.SPACEKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED:
    
    # 1. Spawn ball at X = 2.0 (away from your 4.0 racket) and Z = 10.0 (high in the air)
    ball.worldPosition = [2.0, 0.0, 1.0] 
    
    # 2. Kill all existing momentum
    ball.setLinearVelocity([0.0, 0.0, 0.0], False)
    
    # 3. Apply the upward toss
    toss_power = 10.0  
    forward_toss = -0.0  # Toss it toward the net
    
    ball.setLinearVelocity([forward_toss, 0.0, toss_power], False)
