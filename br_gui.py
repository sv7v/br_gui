'''
Project 'Browser GUI for Brython' (BG)
'''
from browser    import *
from pair_iterator  import *
from browser        import svg

from math           import *
from itertools      import *

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
	# Координаты математики
#	def __init__(self, ...):
#	def draw(self, canvas, x_min, y_min, x_max, y_max):
#		'''Минимальные и максимальные координаты
#		соответствующие 'рамке' графика.'''
#	def getSize(self):
#		'''Минимальные и максимальные координаты для этого объекта'''

	def getFrame(): return 0.1, 0.1, 0.9, 0.9

	def dashes(mi, ma):
		a = (ma - mi)/10
		b = log(a, 10)
		c = floor(b)
		d = c + log(5,10)
		if d < b:
			# e = d
			f = 5 * 10**c  # f = 10**e
		else:
			e = c
			f = 10**c      # f = 10**e

		g = ceil(mi / f)
		h = tuple(takewhile(lambda j: j[0]<ma,
		                    map(lambda i:(f*i,i),
		                        count(g))))[-1][1]
		return f, range(g, h+1)

	def _percent(mi, x, ma, p0, p1):
		return p0 + (p1-p0)*(x-mi)/(ma-mi)

	def percent_x(mi, x, ma): x0, y0, x1, y1 = BG_Item.getFrame(); return BG_Item._percent(mi, x, ma, x0, x1)
	def percent_y(mi, y, ma): x0, y0, x1, y1 = BG_Item.getFrame(); return BG_Item._percent(mi, y, ma, y0, x1)
#class BG_Item:

class BG_Frame(BG_Item):
	def draw(self, canvas, x_min, y_min, x_max, y_max):
		x0, y0, x1, y1 = BG_Item.getFrame()
		canvas.line(x0, y0, x0, y1)
		canvas.line(x0, y1, x1, y1)
		canvas.line(x1, y1, x1, y0)
		canvas.line(x1, y0, x0, y0)

		step, r = BG_Frame.dashes(x_min, x_max)
		for i in r:
			x = BG_Item.percent_x(x_min, step*i, x_max)
			canvas.line(x, y1, x, y1+0.02)          # верхняя
			canvas.line(x, y0, x, y0-0.02)          # нижняя

		step, r = BG_Frame.dashes(y_min, y_max)
		for i in r:
			y = BG_Item.percent_y(y_min, step*i, y_max)
			canvas.line(x0-0.02, y, x0,      y)     # левая
			canvas.line(x1     , y, x1+0.02, y)     # правая

	def getSize(self):
		return None, None, None, None

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
			canvas.line(BG_Item.percent_x(x_min, x0, x_max),
			            BG_Item.percent_y(y_min, y0, y_max),
			            BG_Item.percent_x(x_min, x1, x_max),
			            BG_Item.percent_y(y_min, y1, y_max))

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
		if self._x_min == None or x_min != None and x_min < self._x_min        : self._x_min = x_min
		if self._x_max == None or x_max != None and         self._x_max < x_max: self._x_max = x_max

		if self._y_min == None or y_min != None and y_min < self._y_min        : self._y_min = y_min
		if self._y_max == None or y_max != None and         self._y_max < y_max: self._y_max = y_max

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
