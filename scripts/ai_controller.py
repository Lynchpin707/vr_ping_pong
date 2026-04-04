import bge

cont = bge.logic.getCurrentController()
ai_paddle = cont.owner
scene = bge.logic.getCurrentScene()

# Make sure your ball is named exactly "Ball" in the outliner
ball = scene.objects.get("Ball")

if ball:
    # 1. Difficulty Setting (Higher = faster reaction)
    speed = 0.08 
    
    # 2. Find the ball's Left/Right position
    target_y = ball.worldPosition.y
    current_y = ai_paddle.worldPosition.y
    
    # 3. Move toward the ball smoothly
    ai_paddle.worldPosition.y += (target_y - current_y) * speed
    
    # 4. Lock Position (Keep it on its side of the net)
    ai_paddle.worldPosition.x = 6.0  # Change to match your AI's starting X position
    ai_paddle.worldPosition.z = 1.0  # Change to match table height
    
    # 5. Clamp to table width so it doesn't float away
    ai_paddle.worldPosition.y = max(-4.0, min(4.0, ai_paddle.worldPosition.y))