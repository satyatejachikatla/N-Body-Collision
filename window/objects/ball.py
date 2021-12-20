import pygame
import numpy as np

class Ball:
	def __init__(self,screen,color,radius,initPosition,velocity,acceleration):
		self.screen = screen
		self.color = color

		self.radius = radius
		self.position = initPosition

		self.mass = self.radius # Say mass proportional to radius

		self.velocity = velocity
		self.acceleration = acceleration

	def draw(self):
		pygame.draw.circle(self.screen, self.color, self.position.tolist(), self.radius)
