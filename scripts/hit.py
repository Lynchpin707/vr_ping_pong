import bge

cont = bge.logic.getCurrentController()
racket = cont.owner
collision = cont.sensors["Collision"]

if collision.positive:
    # Grab the ball that we just collided with
    ball = collision.hitObjectList[0]
    
    # 1. Kill the ball's current momentum completely
    ball.setLinearVelocity([0.0, 0.0, 0.0], False)
    
    # 2. Apply a perfect hit! 
    # X = Forward over the net, Y = Left/Right (keep it 0 for straight), Z = Upward arc
    forward_power = 12.0 
    upward_power = 4.0
    
    # 3. Send the ball flying
    ball.setLinearVelocity([forward_power, 0.0, upward_power], False)