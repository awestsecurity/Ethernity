import math						# spiral calculations
import random					# local connections

class Landmark():

	_center = (128,118)
	_spiralwidth = 9.3
	_id = 0
	
	_likeliness = 0.9
	
	def __str__(self):
		return "%s, %s" % (self.id,self.name)

	def __repr__(self):
		return "object %s, %s, at %i,%i, has %i points" % (self.id,self.name,self.origin[0],self.origin[1],len(self.points))

	def __eq__(self, other):
		return self.id == other

	def __cmp__(self, other):
		return self.id == other

	def __init__(self,points,prompt = False, connect = False, name = "Unkown", color = "#ffffff"):
		self.id = type(self)._id
		type(self)._id += 1
		self.name = name
		
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
		self._connected = False
		self.connect = connect
		self.counter = 0
		self.connectPointIndexes = []
		self.connectedObject = None
		self.distance = random.uniform(2.5,6.5)
		self.likeliness = 0.9
		
		if connect:
			self.set_connections()
			more = True if random.random() < type(self)._likeliness else False
			if more:
				self.generate_next_post()
			else:
				self.connect = False
				type(self)._likeliness = 0.9

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
			if self.scale < 1 :
				self.scale += 0.05
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
		if self.connect:
			self.counter += 1
			self.generate_next_post();

	def get_points(self): #Returns all local points in world space
		output = []
		if (self._connected and self.counter > self.distance):
			self.update_connections()
		for point in self.points:
			output.append((point[0]*self.scale+self.origin[0],point[1]*self.scale+self.origin[1]))
		return output

	def get_point(self, p): #Returns a local point in world space
		x = p[0]+self.origin[0]
		y = p[1]+self.origin[1]
		return ( (x,y) )

	def set_point(self, p): #Returns a world point in local space
		x = p[0]-self.origin[0]
		y = p[1]-self.origin[1]
		return ( (x,y) )

	def add_point(self, p, local=True):
		if not local:
			x = p[0]-self.origin[0]
			y = p[1]-self.origin[1]
			self.points.append((x,y))
		else:
			self.points.append(p)

	def set_connections(self,numConnections = 2):
		i = 0
		while (i < numConnections):
			rand = random.uniform(0.2,0.9)
			x = self.get_lerped(self.points[0][0],self.points[1][0],rand)
			y = self.get_lerped(self.points[0][1],self.points[1][1],rand)
			self.add_point( (x,y) )
			self.connectPointIndexes.append( len(self.points)-1 )
			i += 1
	
	def generate_next_post(self):
		if ( not self._connected and self.counter > self.distance ):
			points = []
			points.append( (0,0) )
			points.append( (random.random()*-5+2.5,random.random()*-3-9 ) )
			type(self)._likeliness -= 0.1
			self.connectedObject = Landmark(points,False,True)
			self._connected = True
			self.add_point(self.connectedObject.points[self.connectedObject.connectPointIndexes[0]])

	def update_connections(self):
		numPoints = len(self.points)
		index = self.connectedObject.connectPointIndexes[0]
		pointInOtherLocalSpace = self.connectedObject.points[index]
		pointInWorldSpace = self.connectedObject.get_point( pointInOtherLocalSpace )
		pointInLocalSpace = self.set_point( pointInWorldSpace )
		self.points[numPoints-1] = pointInLocalSpace

	def get_lerped (self, outMin, outMax, input ):
		return outMin + (outMax - outMin) * input


class Prefab():

	barn = ([(-15,0),(-15,-25),(15,-25),(15,0),(-15,-25),(0,-40),(15,-25)],True,False,"Barn")
	fencePost = ([(0,0),(-2,-12)],False,True,"Fence Post")