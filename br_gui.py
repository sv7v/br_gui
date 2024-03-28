'''
Project 'Browser GUI for Brython' (BG)
'''
from browser    import *
from pair_iterator  import *
from browser        import svg

class BG_Table:
	def __init__(self, x):
		self._table = html.TABLE()
		for r in x:
			tr = html.TR()
			for d in r:
				tr <= html.TD(d)
			self._table <= tr
	def get(self):
		return self._table
#class BG_Table:

class BG_LocalFile:
	def __init__(self, inputId, func):
		btn = document[inputId]

		@bind(btn, 'input')
		def file_read(ev):
			def onload(event):
				func(event.target.result)

			# Get the selected file as a DOM File object
			file = btn.files[0]
			# Create a new DOM FileReader instance
			reader = window.FileReader.new()
			# Read the file content as text
			reader.readAsText(file)
			reader.bind('load', onload)
#class BG_LocalFile:

class BG_CanvasBase:
	pass
#	def line(self, x0, y0, x1, y1):
#		'''Координаты в долях. (0;0) -- левый нижний угол 'холста'.
#		(1;1) -- правый верхний угол 'холста'.'''

class BG_HtmlCanvas(BG_CanvasBase):
	def __init__(self, canvas_id):
		c = self.__context = document[canvas_id].getContext('2d')

		self.x_size = c.canvas.width
		self.y_size = c.canvas.height

	def line(self, x0, y0, x1, y1):
		def X(x): return round(x*self.x_size)
		def Y(y): return round(self.y_size*(1-y))

		c = self.__context

		c.beginPath()
		c.moveTo(X(x0), Y(y0))
		c.lineTo(X(x1), Y(y1))
		c.stroke()

class BG_SVG(BG_CanvasBase):
	def __init__(self, g_id):
		self._svg_g = document[g_id]
		self.x_size = int(self._svg_g.parent['width'])
		self.y_size = int(self._svg_g.parent['height'])

	def line(self, x0, y0, x1, y1):
		'''Координаты в долях. (0;0) -- левый нижний угол 'холста'.
		(1;1) -- правый верхний угол 'холста'.'''
		def X(x): return str(round(x*self.x_size))
		def Y(y): return str(round(self.y_size*(1-y)))

		self._svg_g <= svg.line(x1=X(x0),
		                        y1=Y(y0),
		                        x2=X(x1),
		                        y2=Y(y1),
		                        stroke_width="1",
		                        stroke="brown")

class BG_Item:
#	def __init__(self, ...):
#	def draw(self, canvas, x_min, y_min, x_max, y_max):
#		'''Минимальные и максимальные координаты
#		соответствующие 'рамке' графика.'''
#	def getSize(self):
#		'''Минимальные и максимальные координаты для этого объекта'''

	def percent(mi, x, ma): return 0.1 + 0.8*(x-mi)/(ma-mi)

class BG_TableFunc(BG_Item):
	def __init__(self, xy):
		'''Координаты математики'''
		self._data = tuple(xy)

		x = tuple(map(lambda i: i[0],
		              self._data))
		y = tuple(map(lambda i: i[1],
		              self._data))

		self._x_min = min(x)
		self._x_max = max(x)
		self._y_min = min(y)
		self._y_max = max(y)

	def draw(self, canvas, x_min, y_min, x_max, y_max):
		'''Минимальные и максимальные координаты
		соответствующие 'рамке' графика.'''
		for (x0,y0),(x1,y1) in pair(self._data):
			canvas.line(BG_Item.percent(x_min, x0, x_max),
			            BG_Item.percent(y_min, y0, y_max),
			            BG_Item.percent(x_min, x1, x_max),
			            BG_Item.percent(y_min, y1, y_max))

	def getSize(self):
		'''Минимальные и максимальные координаты для этого объекта'''
		return (self._x_min,
		        self._y_min,
		        self._x_max,
		        self._y_max)
#class BG_TableFunc(BG_Item):

class BG_Decart:
	def flatten(*x):
		'''flatten nested list/tuple'''
		for i in x:
			try:
				for j in BG_Decart.flatten(*i):
					yield j
			except TypeError:
				yield i

	def __min_max(self, x_min, y_min, x_max, y_max):
		if not (self._x_min != None and self._x_min < x_min): self._x_min = x_min
		if not (self._y_min != None and self._y_min < y_min): self._y_min = y_min

		if not (self._x_max != None and x_max < self._x_max): self._x_max = x_max
		if not (self._y_max != None and y_max < self._y_max): self._y_max = y_max

	def __init__(self, canvas, *args):
		self._canvas = canvas

		self._data = args

		self._x_min = None
		self._y_min = None
		self._x_max = None
		self._y_max = None

	def draw(self, *args):
		a = tuple(BG_Decart.flatten(self._data, args))

		for i in a:
			b = i.getSize()
			self.__min_max(*b)

		for i in a:
			i.draw(self._canvas, self._x_min,
			                     self._y_min,
			                     self._x_max,
			                     self._y_max)
#class BG_Decart:
