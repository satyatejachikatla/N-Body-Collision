class Background:
	def __init__(self,screen,color=(0,0,0)):
		self.color = color
		self.screen = screen

	def draw(self):
		self.screen.fill(self.color)