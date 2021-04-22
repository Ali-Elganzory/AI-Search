class Particle(object):
	"""docstring for Particle"""
	def __init__(self, position, velocity):
		super(Particle, self).__init__()
		self.__position = position
		self.__velocity = velocity

	@property
	def position(self):
		return self.__position

	@position.setter
	def position(self, position):
		self.__position = position
	
	@property
	def velocity(self):
		return self.__velocity

	@velocity.setter
	def velocity(self, velocity):
		self.__velocity = velocity

	def update(self):
		self.__position += self.__velocity

	def accelerate(self, acceleration):
		self.__velocity += acceleration
