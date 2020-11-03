
class Obj(object):
	"""docstring for Obj"""
	def __init__(self, filename):
		with open(filename) as f:
			self.lines = f.read().splitlines()

		self.vertices = []
		self.faces = []
		self.read()

	def read(self):
		for line in self.lines:
			try:
				prefix, value = line.split(' ', 1)
				if prefix == 'v':
					vertix = []
					for item in value.split(' '):
						if item!='':
							vertix.append(float(item))
					self.vertices.append(
						vertix
					)
				elif prefix == 'f':
					face = []
					for item in value.split(' '):
						if item!='':
							point = []
							for coordinate in item.split('/'):
								point.append(int(coordinate))
							face.append(point)
					self.faces.append(
						face
					)
			except Exception as e:
				x = e  												