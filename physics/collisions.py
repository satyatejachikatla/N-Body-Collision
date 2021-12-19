import numpy as np
from physics.utils import length
from window.objects.ball import Ball

def detectBallToBallCollision(ball1: Ball,ball2: Ball):
    if length(ball1-ball2) < ball1.radius + ball2.radius:
        return True
    return False

def detectBallToWallCollision(ball: Ball):
    windowSize = ball.screen.get_size()

    xRange = range(0,windowSize[0])
    yRange = range(0,windowSize[1])

    leftWindowCollision = False
    rightWindowCollision = False
    topWindowCollision = False
    bottomWindowCollision = False

    if ball.position[0] - ball.radius <= xRange.start:
        leftWindowCollision = True
    if ball.position[0] + ball.radius >= xRange.stop:
        rightWindowCollision = True

    if ball.position[1] - ball.radius <= yRange.start:
        topWindowCollision = True
    if ball.position[1] + ball.radius >= yRange.stop:
        bottomWindowCollision = True

    return {
        'left' : leftWindowCollision,
        'right' : rightWindowCollision,
        'top' : topWindowCollision,
        'bottom' : bottomWindowCollision
    }
