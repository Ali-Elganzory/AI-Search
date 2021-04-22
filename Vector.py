import javascript

class Vector(object):
	"""docstring for Vector"""
	def __init__(self, x, y):
		super(Vector, self).__init__()
		self.__x = x
		self.__y = y

	def __add__(self, o):
		return Vector(x=self.__y + o.y, y=self.__y + o.y)

	@property
	def x(self):
		return self.__x

	@x.setter
	def x(self, x):
		self.__x = x

	@property
	def y(self):
		return self.__y

	@y.setter
	def y(self, y):
		self.__y = y

	@property
	def angle(self):
		return 0 if self.x == 0 else javascript.Math.atan2(self.y, self.x)
