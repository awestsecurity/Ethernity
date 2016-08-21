from tkinter import *			# canvas and drawing
from threading import Timer		# scheduling events
import math						# spiral calculations
import os
import random as r

# My Scripts
from player import Player
from rotate import Rotation

#create a window for spiral landscape
window = Tk()
window.title("Ethernity")
window.geometry("256x256+30+340")
window.configure(background="#000000")
#window.wm_iconbitmap('alien.ico')

#create a window for text
window2 = Toplevel(window, width="512",height="256",bg="#000000")
window2.title("Hello World")
window2.geometry("512x256+310+310")


center = (128,118)
sPoints = list()
sPoints2 = list()
sMove = False
gameReady = False
direction = 0
playerGraphic = None
player = Player()

seed = int(r.random()*1000)
seedCounter = 0
print ("world seed:",seed)

testPoints = [(-15,0),(-15,-25),(15,-25),(15,0),(-15,-25),(0,-40),(15,-25)]
landmarks = []
landmarks.append( Rotation(testPoints) )


def draw_player():
	playerImage = PhotoImage(master=spiral, width=player.x,height=player.y)
#	os.chdir(os.path.dirname(sys.argv[0])) #change directory to local folder.
	while True:
		for t in player.get_frame():
			playerImage.put(player.color,t)
#		player = PhotoImage(width=10,height=30,file='player.gif')
		return playerImage
		
def draw_objects():
	for obj in landmarks:
		spiral.create_line(obj.get_points(),fill=obj.color,width=2,capstyle=ROUND,tags="clear")
		obj.set_next_position();
		if (obj.origin[0] < 130 and obj.origin[1] > 200 and obj.triggered == False):
			obj.triggered = True
			put_text(obj.string)
		if (obj.origin[0] >= 285 or obj.origin[1] >= 285):
			landmarks.remove(obj)

def put_text(string):
	text.config(state=NORMAL)
	text.insert("1.0", string+"\n")
	text.config(state=DISABLED)

def spawn_object():
	alpha = 'abcdefghijklmnopqrstuvwxyz'
	newObj = Rotation(testPoints)
	newObj.string = r.choice(alpha)
	landmarks.append( newObj )

def random_generate():
	global seed
	global seedCounter
	r.seed(seed + seedCounter)
	seedCounter += 1
	if (r.random() < 0.05):
		spawn_object()

i = 0
def draw_next_line(stepTime = 0.025):
	t = Timer(stepTime, draw_next_line)
	t.start()
	global sPoints
	global center
	global i
	var = next(pointsGenerator)
	var2 = next(pointsGenerator2)
	sPoints.append(var[0]+center[0])
	sPoints.append(var[1]+center[1])
	sPoints2.append(var2[0]+center[0])
	sPoints2.append(var2[1]+center[1])
	spiral.create_line(sPoints2[i-2],sPoints2[i-1],sPoints2[i],sPoints2[i+1],fill="#800000",width=12,capstyle=ROUND,smooth=True)
	spiral.create_line(sPoints[i-2],sPoints[i-1],sPoints[i],sPoints[i+1],fill="#ffffff",width=6,capstyle=ROUND,smooth=True)
#	spiral.create_line(sPoints[i-2],sPoints[i-1],sPoints[i],sPoints[i+1],fill="#ffffff",width=8,dash=(1,10),capstyle=ROUND,smooth=True,tags="grass")
	i+=2
	if(sPoints[i] > 300 or sPoints[i] < -50):
		t.cancel()
		print ("spiral drawn")
		global gameReady
		global playerGraphic
		gameReady = True
		draw_objects()
		playerGraphic = draw_player()
		spiral.create_image(123,236, image=playerGraphic, state="normal", tags="clear")
		print ("player drawn")

def rotate_spiral():
	t = Timer(0.4, rotate_spiral)
	t.start()
	clear_canvas("object")
	global sMove
	newPoints = rotate_points(sPoints)
	spiral.create_line(newPoints,fill="#ffffff",width=7,capstyle=ROUND)
	sPoints = newPoints
	if sMove == False:
		t.cancel()
		
def zoom_spiral(): #canvas.scale? resize window or crop?
	xOrigin = 256
	yOrigin = 256
	xZoom = 512
	yZoom = 512
	
def Update():
	global sMove
	global playerGraphic
	if sMove:
		t = Timer(0.4, Update)
		t.start()
		clear_canvas("clear")
		draw_objects()
		playerGraphic = draw_player()
		spiral.create_image(123,236, image=playerGraphic, state="normal", tags="clear")
		random_generate()
		if sMove == False:
			t.cancel()
	
def stop_spiral(event):
	global sMove
	sMove = False
	
def move_spiral_forward(event):
	global sMove
	global direction
	if sMove == False:
		direction = 1
		sMove = True
		Update()

def move_spiral_backward(event):
	global sMove
	global direction
	if sMove == False:
		direction = -1
		sMove = True
		Update()
		
def clear_canvas(s = "all"):
	global spiral
	spiral.delete(s)

def get_spiral_points(arc=25.0, separation=60):
	
	global center
	
	def p2c(r, phi): #polar to cartesian
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
		
#Setup Text Window
text = Text(window2,background="#000000",foreground="#ffffff",state=DISABLED,width="64",wrap="word")
text.pack()
#Setup Spiral Landscape
spiral = Canvas(window,width=(256),height=(256),background="#000000")
spiral.pack()
pointsGenerator = get_spiral_points()
pointsGenerator2 = get_spiral_points(30,60)
var = next(pointsGenerator)
var2 = next(pointsGenerator2)
sPoints.append(var[0]) # Store origin point
sPoints.append(var[1]) # Store origin point
sPoints2.append(var2[0])
sPoints2.append(var2[1])
draw_next_line()

#Setup Bindings
spiral.bind("<Right>", move_spiral_forward)
spiral.bind("<KeyRelease-Right>", stop_spiral)
spiral.bind("<Left>", move_spiral_backward)
spiral.bind("<KeyRelease-Left>", stop_spiral)
spiral.focus_set()

#draw the window, and start the 'application'
window.mainloop()