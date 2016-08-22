import math						# spiral calculations
import random					# local connections

class Landmark():

	_center = (128,118)
	_spiralwidth = 9.3

	def __init__(self,points,prompt = False, connect = False, color = "#ffffff"):
		#Visual necessities
		self.points = points
		self.origin = type(self)._center
		self.scale = 0.1
		self.color = color
		self.nextPos = self.__rotate_origin()
		
		#Stuff for prompting landmarks
		self.prompt = prompt
		self.triggered = False
		self.stopMovement = False
		self.string = "!"

		#Stuff for fences and other connecting landmarks
		self.connect = connect
		self.counter = 0
		self.connectPoints = []
		self.connectedObject = None
		self.distance = random.random()*5.0+2
		
		if (connect):
			self.set_connections()
			more = True if random.random() < 0.66 else False
			if (more):
				self.generate_next_post()
			else:
				self.connect = False

	# parametric equation of spiral:  x(t) = at cos(t), y(t) = at sin(t)
	def __rotate_origin(self): #assumes even number of points
		center = self.origin
		a = type(self)._spiralwidth
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
			#print(t)

	def __rotate_points(self,degrees):
		self.newPoints = []
		for point in self.points:
			x = point[0]*(math.cos(degrees)) - point[1]*(math.sin(degrees))
			y = point[1]*(math.cos(degrees)) + point[0]*(math.sin(degrees))
			self.newPoints.append((x,y))
		self.points = self.newPoints

	def set_next_position(self):
		self.origin = next(self.nextPos)
		if(self.connect):
			self.counter += 1
			self.generate_next_post()
		

	def get_points(self):
		output = []
		for point in self.points:
			output.append((point[0]*self.scale+self.origin[0],point[1]*self.scale+self.origin[1]))
		return output

	def get_point(self, p):
		x = p[0]+self.origin[0]
		y = p[1]+self.origin[1]
		return ( (x,y) )

	def add_point(self, p, local=True):
		if (local != True):
			x = p[0]-self.origin[0]
			y = p[1]-self.origin[1]
			self.points.append((x,y))
		else:
			self.points.append(p)

	def set_connections(self,numConnections = 2):
		i = 0
		while (i < numConnections):
			rand = random.random()
			x = self.get_lerped(self.points[0][0],self.points[0][1],rand)
			y = self.get_lerped(self.points[1][0],self.points[1][1],rand)
			self.connectPoints.append( (x,y) )
			i += 1
	
	def generate_next_post(self):
		if (self.counter > self.distance):
			points = []
			points.append( (0,0) )
			points.append( (random.random()*-5+2.5,random.random()*-3-9 ) )
			self.connectedObject = Landmark(points,False,True)
			self.add_point(self.connectPoints[0])
			newpoint = self.connectedObject.get_point(self.connectedObject.connectPoints[0])
			self.add_point( newpoint,False )
			newpoint = self.connectedObject.get_point(self.connectedObject.connectPoints[1])
			self.add_point( newpoint,False )
			self.add_point(self.connectPoints[1])
			self.connect = False

	def get_lerped (self, outMin, outMax, input ):
		return outMin + (outMax - outMin) * input


class Prefab():

	barn = ([(-15,0),(-15,-25),(15,-25),(15,0),(-15,-25),(0,-40),(15,-25)],True,False)
	fencePost = ([(0,0),(-2.5,-12)],False,True)