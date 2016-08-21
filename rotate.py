import math						# spiral calculations

class Rotation():

	#radiusOffset = 3 #only needs to be set once on the first Rotation object
	angle = 0.05

	def __init__(self,points,color = "#ffffff"):
		self.points = points
		self.origin = (128,118)
		self.triggered = False
		self.string = "An old barn"
		self.scale = 0.1
		self.color = color
		self.nextPos = self.__rotate_origin()
		#Rotation.radiusOffset = radius


	# parametric equation of spiral:  x(t) = at cos(t), y(t) = at sin(t)
	def __rotate_origin(self): #assumes even number of points
		center = self.origin
		a = 9.2
		t = 0.0
		j = 1.0
		while True:
			x = center[0] + (a*t*math.cos(t))
			y = center[1] + (a*t*math.sin(t))
			yield [x,y,x,y]
			t = math.sqrt(t+j)
			self.__rotate_points(0.768/t)
			j += 1.5
			if (self.scale < 1):
				self.scale += 0.025
			print(t)

	def __rotate_points(self,degrees):
		self.newPoints = []
		for point in self.points:
			x = point[0]*(math.cos(degrees)) - point[1]*(math.sin(degrees))
			y = point[1]*(math.cos(degrees)) + point[0]*(math.sin(degrees))
			self.newPoints.append((x,y))
		self.points = self.newPoints

	def set_next_position(self):
		self.origin = next(self.nextPos)

	def get_points(self):
		output = []
		for point in self.points:
			output.append((point[0]*self.scale+self.origin[0],point[1]*self.scale+self.origin[1]))
		return output

	def add_point(x,y,local=True):
		if (local != True):
			x-=self.origin[0]
			y-=self.origin[1]
		self.points.append((x,y))