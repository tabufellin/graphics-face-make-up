#render by Sebastian
import struct
import random
from encoder import *
from math_things import *
from obj import Obj

def color(r, g, b):
  return bytes([b, g, r])


BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)


class Render(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.current_color = WHITE
		self.clear()

	def clear(self):
		self.pixels = [
	      	[BLACK for x in range(self.width)] 
	      	for y in range(self.height)
	    ]

	def write(self, filename):
	    f = open(filename, 'bw')

	    # File header (14 bytes)
	    f.write(char('B'))
	    f.write(char('M'))
	    f.write(dword(14 + 40 + self.width * self.height * 3))
	    f.write(dword(0))
	    f.write(dword(14 + 40))

	    # Image header (40 bytes)
	    f.write(dword(40))
	    f.write(dword(self.width))
	    f.write(dword(self.height))
	    f.write(word(1))
	    f.write(word(24))
	    f.write(dword(0))
	    f.write(dword(self.width * self.height * 3))
	    f.write(dword(0))
	    f.write(dword(0))
	    f.write(dword(0))
	    f.write(dword(0))

	    
	    for x in range(self.height):
	    	for y in range(self.width):
	    		f.write(self.pixels[x][y])

	    f.close()

	def display(self, filename='out.bmp'):
	    self.write(filename)

	    try:
	    	from wand.image import Image
	    	from wand.display import display
	    	with Image(filename=filename) as image:
	        	display(image)
	    except ImportError:
	      	pass 

	def set_color(self, color):
		self.current_color = color

	def point(self, x, y, color = None):
	    try:
	    	self.pixels[y][x] = color or self.current_color
	    except:
	    	pass
    
	def line(self, start, end, color = None):
	    x1, y1 = start.x, start.y
	    x2, y2 = end.x, end.y

	    dy = abs(y2 - y1)
	    dx = abs(x2 - x1)
	    steep = dy > dx

	    if steep:
	        x1, y1 = y1, x1
	        x2, y2 = y2, x2

	    if x1 > x2:
	        x1, x2 = x2, x1
	        y1, y2 = y2, y1

	    dy = abs(y2 - y1)
	    dx = abs(x2 - x1)

	    offset = 0
	    threshold = dx

	    y = y1
	    for x in range(x1, x2 + 1):
	        if steep:
	            self.point(y, x, color)
	        else:
	            self.point(x, y, color)
	        
	        offset += dy * 2
	        if offset >= threshold:
	            y += 1 if y1 < y2 else -1
	            threshold += dx * 2

	def triangle(self, A, B, C, color=None):
	    bbox_min, bbox_max = bbox(A, B, C)

	    for x in range(bbox_min.x, bbox_max.x + 1):
	      for y in range(bbox_min.y, bbox_max.y + 1):
	        w, v, u = barycentric(A, B, C, V2(x, y))
	        if w < 0 or v < 0 or u < 0:  
	          continue
	        
	        self.point(x, y, color)

	def transform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):

	    return V3(
	      round((vertex[0] + translate[0]) * scale[0]),
	      round((vertex[1] + translate[1]) * scale[1]),
	      round((vertex[2] + translate[2]) * scale[2])
	    )
	    
	def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1)):

	    model = Obj(filename)

	    light = V3(0,0,1)

	    for face in model.faces:
	        vcount = len(face)

	        if vcount == 3:
	          f1 = face[0][0] - 1
	          f2 = face[1][0] - 1
	          f3 = face[2][0] - 1

	          a = self.transform(model.vertices[f1], translate, scale)
	          b = self.transform(model.vertices[f2], translate, scale)
	          c = self.transform(model.vertices[f3], translate, scale)

	          normal = norm(cross(sub(b, a), sub(c, a)))
	          intensity = dot(normal, light)
	          grey = round(255 * intensity)
	          if grey < 0:
	            continue  
	          
	          self.triangle(a, b, c, color(grey, grey, grey))
	        else:
	          # assuming 4
	          f1 = face[0][0] - 1
	          f2 = face[1][0] - 1
	          f3 = face[2][0] - 1
	          f4 = face[3][0] - 1   

	          vertices = [
	            self.transform(model.vertices[f1], translate, scale),
	            self.transform(model.vertices[f2], translate, scale),
	            self.transform(model.vertices[f3], translate, scale),
	            self.transform(model.vertices[f4], translate, scale)
	          ]

	          normal = norm(cross(sub(vertices[0], vertices[1]), sub(vertices[1], vertices[2])))
	          intensity = dot(normal, light)
	          grey = round(255 * intensity)
	          if grey < 0:
				#no se pinta
	            continue 

	          
	  
	          A, B, C, D = vertices 
	        
	          self.triangle(A, B, C, color(grey, grey, grey))
	          self.triangle(A, C, D, color(grey, grey, grey))