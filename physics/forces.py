from typing import List

from itertools import combinations
import numpy as np
from physics.collisions import detectBallToBallCollision, detectBallToWallCollision
from physics.utils import length
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

    #Position update
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

    #Velocity update
    ball.velocity[1] = -ball.velocity[1]

def resolveBallToWallCollisionVertical(ball:Ball,deltaTime,collision):
    windowSize = ball.screen.get_size()
    currentPos = ball.position
    previousPos = getPrevPosition(ball,deltaTime)

    #Position update
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

    #Velocity update
    ball.velocity[0] = -ball.velocity[0]

def resolveBallToBallCollision(ball1:Ball,ball2:Ball):
    windowSize = ball1.screen.get_size()

    #Position update
    # TODO : Check

    #Velocity update
    # ball2FinalVelocity = 2*(ball2.mass)/(ball1.mass + ball2.mass)*(ball1.velocity - ball2.velocity).dot(ball1.position - ball2.position)/(length(ball1.position - ball2.position)**2)*(ball1.position - ball2.position)
    # ball1FinalVelocity = 2*(ball1.mass)/(ball1.mass + ball2.mass)*(ball2.velocity - ball1.velocity).dot(ball2.position - ball1.position)/(length(ball2.position - ball1.position)**2)*(ball2.position - ball1.position)

    #Velocity update
    ball1FinalVelocity = (ball1.mass - ball2.mass)/(ball1.mass + ball2.mass)*ball1.velocity + 2*(ball2.mass)/(ball1.mass + ball2.mass)*ball2.velocity
    ball2FinalVelocity = (ball2.mass - ball1.mass)/(ball1.mass + ball2.mass)*ball2.velocity + 2*(ball1.mass)/(ball1.mass + ball2.mass)*ball1.velocity


    ball1.velocity = ball1FinalVelocity
    ball2.velocity = ball2FinalVelocity


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
        
        # print(f'Pos : {ball.position.tolist()} , Vel : {ball.velocity.tolist()} , Col : {collisions}')

    for balls in combinations(objects,2):
        if detectBallToBallCollision(balls[0],balls[1]):
            resolveBallToBallCollision(balls[0],balls[1])

