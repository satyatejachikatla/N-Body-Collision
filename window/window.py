import pygame
import datetime
import random
import numpy as np
from collections import OrderedDict
from physics.forces import resolveCollision, updatePosition, updateVelocity

from physics.utils import unit_vector

from .objects import background
from .objects import ball

def genBall(screen,position):
	randomColor = (
		random.randint(20,255),
		random.randint(20,255),
		0,
	)

	windowSize = screen.get_size()
	minWindowDimension = min(windowSize)

	# Radius
	ballSize = minWindowDimension/75

	# Radius Deviation
	ballSize = ballSize + int(random.randint(-50,50)*ballSize/200)

	# Forces
	baseVelocity = 50
	velocity = unit_vector(np.random.uniform(-1,1,2))*baseVelocity

	acceleration = np.zeros(2)

	return ball.Ball(	screen=screen,
						color=randomColor,
						radius=ballSize,
						initPosition=position,
						velocity=velocity,
						acceleration=acceleration
					)

class Window():

	def __init__(self):
		self.pygameInit()
		self.objectsInit()

	def pygameInit(self):
		self.DISPLAY_WINDOW_X , self.DISPLAY_WINDOW_Y = (1000,700)
		self.DISPLAY_WINDOW = (self.DISPLAY_WINDOW_X,self.DISPLAY_WINDOW_Y)
		#Game init
		pygame.init()

		#Screen Init
		pygame.display.set_caption("NBody Collision")
		self.screen = pygame.display.set_mode(self.DISPLAY_WINDOW)

		self.gameLoopRunning = False
		self.prevTime = datetime.datetime.now()
		self.deltaTime = self.prevTime - self.prevTime

	def objectsInit(self):
		self.objects = OrderedDict({
			'screenBg' : background.Background(self.screen,color=(0x20,0x2A,0x44)),
			
			'ball0' : genBall(self.screen,np.array([100,100])),
			'ball1' : genBall(self.screen,np.array([200,200])),
		})

		self.currBallIdx = 2

	def keyEvents(self):
		# All keys pressed, is a dictionary of bools of all keys
		key=pygame.key.get_pressed()


		# All Pygame Event handling
		for event in pygame.event.get():

			#Generate ball on mouseclick
			if event.type == pygame.MOUSEBUTTONUP :
				pos = pygame.mouse.get_pos()
				self.objects[f'ball{self.currBallIdx}'] = genBall(self.screen,np.array(pos))
				self.currBallIdx += 1

			if event.type == pygame.QUIT:
				self.gameLoopRunning = False

	def updatePhysics(self):
		allBalls = list( self.objects[objectName] for objectName in self.objects if objectName.startswith('ball'))
		deltaTimeDamp = 1.
		deltaTime = self.deltaTime.total_seconds()*deltaTimeDamp
		updateVelocity(allBalls,deltaTime)
		updatePosition(allBalls,deltaTime)
		resolveCollision(allBalls,deltaTime)

	def draw(self):
		for object in self.objects.values():
			object.draw()

	def gameLoop(self):
		clock = pygame.time.Clock()
		self.gameLoopRunning = True
		self.prevTime = datetime.datetime.now()

		while self.gameLoopRunning:
			self.keyEvents()
			self.updatePhysics()
			self.draw()
			pygame.display.flip()

			# Timing game loop
			self.deltaTime = datetime.datetime.now() - self.prevTime
			self.prevTime = self.prevTime + self.deltaTime
			clock.tick(60)
