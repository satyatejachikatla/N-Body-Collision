from typing import List

import numpy as np
from physics.collisions import detectBallToWallCollision
from window.objects.ball import Ball

def getPrevPosition(ball :Ball,deltaTime):
    previousVelocity = ball.velocity - ball.acceleration*deltaTime
    previousPos = ball.position - previousVelocity*deltaTime
    return previousPos

def updatePosition(objects: List[Ball],deltaTime):
    for ball in objects:
        ball.position = ball.position + ball.velocity*deltaTime

def updateVelocity(objects: List[Ball],deltaTime):
    for ball in objects:
        ball.velocity = ball.velocity + ball.acceleration*deltaTime

def resolveBallToWallCollisionHorizontal(ball:Ball,deltaTime,collision):
    windowSize = ball.screen.get_size()
    currentPos = ball.position
    previousPos = getPrevPosition(ball,deltaTime)

    assert(currentPos[1]-previousPos[1] != 0)
    if collision == 'top':
        matchRadiusValue = ball.radius
    elif collision == 'bottom':
        matchRadiusValue = windowSize[1] - ball.radius

    collisionTime =  (matchRadiusValue-previousPos[1])/(currentPos[1]-previousPos[1])
    collisionPos = previousPos*(1-collisionTime) + currentPos*collisionTime

    verticalVec = np.array([0.,collisionPos[1]-currentPos[1]])

    updatedPos = currentPos + verticalVec*2

    ball.position = updatedPos
    ball.velocity[1] = -ball.velocity[1]

def resolveBallToWallCollisionVertical(ball:Ball,deltaTime,collision):
    windowSize = ball.screen.get_size()
    currentPos = ball.position
    previousPos = getPrevPosition(ball,deltaTime)

    assert(currentPos[0]-previousPos[0] != 0)
    if collision == 'left':
        matchRadiusValue = ball.radius
    elif collision == 'right':
        matchRadiusValue = windowSize[0] - ball.radius

    collisionTime =  (matchRadiusValue-previousPos[0])/(currentPos[0]-previousPos[0])
    collisionPos = previousPos*(1-collisionTime) + currentPos*collisionTime

    horizontalVec = np.array([collisionPos[0]-currentPos[0],0.])

    updatedPos = currentPos + horizontalVec*2

    ball.position = updatedPos
    ball.velocity[0] = -ball.velocity[0]

def resolveCollision(objects : List[Ball],deltaTime):
    if deltaTime == 0:
        return

    for ball in objects:
        collisions = detectBallToWallCollision(ball)

        if collisions['left']:
            resolveBallToWallCollisionVertical(ball,deltaTime,'left')
        if collisions['right']:
            resolveBallToWallCollisionVertical(ball,deltaTime,'right')

        if collisions['top']:
            resolveBallToWallCollisionHorizontal(ball,deltaTime,'top')
        if collisions['bottom']:
            resolveBallToWallCollisionHorizontal(ball,deltaTime,'bottom')
        
        print(f'Pos : {ball.position.tolist()} , Vel : {ball.velocity.tolist()} , Col : {collisions}')