from tkinter import *			# canvas and drawing
from threading import Timer		# scheduling events
import math						# spiral calculations
import os
import random as r

# My Scripts
from player import Player
from rotate import Landmark, Prefab

#create a window for spiral landscape
window = Tk()
window.title("Ethernity")
window.geometry("256x256+30+340")
window.configure(background="#000000")
#window.wm_iconbitmap('alien.ico')

#create window for portrait
windowFace = Toplevel(window, width="170",height="170",bg="#FFFFFF")
windowFace.title("Portait")
windowFace.geometry("170x170+10+20")

#create a window for text
window2 = Toplevel(window, width="512",height="256",bg="#000000")
window2.title("Hello World")
window2.geometry("512x380+310+210")

center = (128,118)
sPoints = list()
sPoints2 = list()
sMove = False
gameReady = False
direction = 0
playerGraphic = None
drawplayer = None
player = Player()

seed = int(r.random()*1000)
seedCounter = 0
print ("world seed:",seed)

landmarks = []
canvaselements = []
connectinglines = []

dialogue = []
response = False

def draw_player():
	playerImage = PhotoImage(master=spiral, width=player.x,height=player.y)
#	os.chdir(os.path.dirname(sys.argv[0])) #change directory to local folder.
	while True:
		for t in player.get_frame():
			playerImage.put(player.color,t)
#		playerImage = PhotoImage(width=10,height=30,file='player.gif')
		return playerImage
		
def draw_objects():
	for obj in landmarks:
		obj.set_next_position();
	i = 0
	j = 0
	for obj in landmarks:
		coordslist = obj.get_coords()
		spiral.coords(canvaselements[i], coordslist)
		if obj.connectedObject != None:
			if  obj.connect:
				line = generate_connection(obj)
				obj.connect = False
				landmarks.append(obj.connectedObject)
				o = spiral.create_polygon(obj.connectedObject.get_points(),fill=obj.connectedObject.color,width=2)
				canvaselements.append( o )
				connectinglines.append( spiral.create_line(line,fill=obj.connectedObject.color,width=1) )
			else:
				line = generate_connection(obj, False)
				spiral.coords(connectinglines[j], line)
				j += 1
		#Player has reached Object
		if (obj.origin[0] < 130 and obj.origin[1] > 200 and obj.triggered == False):
			obj.triggered = True
			if obj.prompt:
				put_text(obj.string)
			if (obj.stopMovement):
				global sMove
				global gameReady
				global response
				sMove = False
				gameReady = False
				response = True
		#Object has left screen space
		if (obj.origin[0] >= 290 or obj.origin[1] >= 290):
			if obj.connectedObject != None:
				del connectinglines[0]
				j -= 1
			del canvaselements[0]
			spiral.delete(canvaselements[0])
			del landmarks[0]
			i -= 1
		i += 1

def put_text(string):
	lines = string.split("\n")
	for line in lines:
		dialogue.append(line)


def print_text(delay = 0.9):
	t = Timer(delay, print_text)
	t.start()
	if len(dialogue) > 0:
		text.config(state=NORMAL)
		text.insert("1.0", dialogue.pop(0)+"\n")
		text.config(state=DISABLED)


def spawn_object(obj = Prefab.fencePost):
	landmarks.append( Landmark(*obj) )
	o = spiral.create_polygon(landmarks[-1].get_points(),fill=landmarks[-1].color,width=2,tags="landmark")
	canvaselements.append( o )

#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  ##
# # # # SET PROBABILITY OF OBJECTS HERE # # # #
def random_generate():
	global seed
	global seedCounter
	r.seed(seed + seedCounter)
	seedCounter += 1
	if r.random() < 0.04 : spawn_object(Prefab.tree)
	elif r.random() < 0.02 : spawn_object(Prefab.fencePost)
	elif r.random() < 0.01 : spawn_object(Prefab.barn)

#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  ##
# # # #    SET OPENING SCENE HERE       # # # #
i = 0
def draw_next_line(stepTime = 0.01):
	t = Timer(stepTime, draw_next_line)
	t.start()
	global sPoints
	global center
	global i
	var = next(pointsGenerator)
	sPoints.append(var[0]+center[0])
	sPoints.append(var[1]+center[1])
	#spiral.create_line(sPoints[i-2],sPoints[i-1],sPoints[i],sPoints[i+1],fill="#ffffff",width=6,capstyle=ROUND,smooth=True)
	i+=2
	if(sPoints[i] > 300 or sPoints[i] < -50):
		t.cancel()
		print ("spiral drawn")
		global gameReady
		global drawplayer
		global playerGraphic
		draw_objects()
		drawplayer = draw_player()
		playerGraphic = spiral.create_image(123,236, image = drawplayer)
		print ("player drawn")
		put_text("You are here .")
		put_text("You can't see any-thing.\n")
		put_text("It seems you can w a l k .\n")
		gameReady = True

# 
def zoom_spiral(): #canvas.scale? resize window or crop?
	xOrigin = 256
	yOrigin = 256
	xZoom = 512
	yZoom = 512

# # # Run Every Frame
def Update():
	global sMove
	global playerGraphic
	global drawplayer
	if sMove:
		t = Timer(0.12, Update)
		t.start()
		clear_canvas("clear")
		draw_objects()
		drawplayer = draw_player()
		spiral.itemconfig(playerGraphic, image = drawplayer)
		spiral.tag_raise(playerGraphic)
		random_generate()
		if sMove == False or gameReady == False:
			t.cancel()

def stop_spiral(event):
	global sMove
	sMove = False

def move_spiral(event):
	global gameReady
	if gameReady == False : return None
	global sMove
	global direction
	if sMove == False and gameReady:
		direction = 1
		sMove = True
		Update()

def clear_canvas(s = "all"):
	global spiral
	spiral.delete(s)

def get_spiral_points(arc=25.0, separation=60):
	global center
	def p2c(r, phi):    #polar to cartesian
		return (r * math.cos(phi), r * math.sin(phi))
	yield (center[0], center[1])			   # yield a point at origin
	print("origin logged")
	r = arc				   # initialize the next point in the required distance
	b = separation / (2 * math.pi) # find the first phi to satisfy distance of `arc` to the second point
	phi = float(r) / b
	while True:
		yield p2c(r, phi)
		# advance the variables
		# calculate phi that will give desired arc length at current radius
		# (approximating with circle)
		phi += float(arc) / r
		r = b * phi

def generate_connection(landmark, tuple = True):
	line = []
	if tuple:
		line.append(landmark.get_subpoint(0))
		line.append(landmark.connectedObject.get_subpoint(0))
		line.append(landmark.connectedObject.get_subpoint(1))
		line.append(landmark.get_subpoint(1))
	else :
		line.append(landmark.get_subpoint(0)[0])
		line.append(landmark.get_subpoint(0)[1])
		line.append(landmark.connectedObject.get_subpoint(0)[0])
		line.append(landmark.connectedObject.get_subpoint(0)[1])
		line.append(landmark.connectedObject.get_subpoint(1)[0])
		line.append(landmark.connectedObject.get_subpoint(1)[1])
		line.append(landmark.get_subpoint(1)[0])
		line.append(landmark.get_subpoint(1)[1])
	return line

def resume(event, bool):
	global response
	if response:
		global gameReady
		gameReady = bool
		s = "That m a k e s sense." if bool else "Let's not just sit here. This place is interesting. Y \ N"
		s += "\n"
		put_text(s)
		response = not bool
	
#Setup Text Window
text = Text(window2,background="#000000",foreground="#ffffff",state=DISABLED,width="64",wrap="word")
text.pack()
print_text() # text delay per line

#Setup Spiral Landscape
spiral = Canvas(window,width=(256),height=(256),background="#000000")
spiral.pack()	
pointsGenerator = get_spiral_points()
var = next(pointsGenerator)
sPoints.append(var[0]) # Store origin point
sPoints.append(var[1]) # Store origin point
draw_next_line()

#Setup Bindings
spiral.bind("<Right>", move_spiral)
spiral.bind("<KeyRelease-Right>", stop_spiral)
spiral.bind("<Left>", move_spiral)
spiral.bind("<KeyRelease-Left>", stop_spiral)
spiral.bind("<y>", lambda event, arg=True:resume(event, arg))
spiral.bind("<n>", lambda event, arg=False:resume(event, arg))
spiral.focus_set()

# # #Testing portrait window - make dynamic system and delete this. # # #
tmpphoto = PhotoImage(file = "P-skull.png")
wf = Label(windowFace, image=tmpphoto)
wf.pack()
#end test

#draw the window, and start the 'application'
window.mainloop()