'''
Project 'Browser GUI for Brython' (BG)
'''
from browser    import *
from pair_iterator  import *
from browser        import svg

from math           import *
from itertools      import *
from uuid           import uuid4

def flatten(*x):
	'''flatten nested list/tuple'''
	for i in x:
		try:
			for j in flatten(*i):
				yield j
		except TypeError:
			yield i

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

class BG_LocalTextFile:
	def __init__(self, callback):
		self._data = html.INPUT(type='file')

		def input(event):
			def load(event):
				callback(event.target.result)

			file = self._data.files[0]

			reader = window.FileReader.new()
			reader.readAsText(file)
			reader.bind('load', load)

		self._data.bind('input', input)

	def get(self):
		return self._data
#class BG_LocalTextFile:

class BG_CheckBox:
	def __init__(self, hook, title=''):
		self._id  = str(uuid4())
		self._data = html.INPUT(type='checkbox', onchange=hook, title=str(title), id=self._id)
	def get(self):
		return self._data
	def getState(self):
		return document[self._id].checked
	def set(self, state=True):
		document[self._id].checked = state

class BG_Property:          pass

class BG_LogY(BG_Property): pass

class BG_Affinis(BG_Property):
	def __init__(self, tg=0):
		self._tg = tg
	def tg(self):
		return self._tg

class BG_CanvasBase:
	LEFT   = 0x1
	BOTTOM = 0x1 << 1
	RIGHT  = 0x1 << 2
	TOP    = 0x1 << 3
#	def clear(self):
#	def line(self, x0, y0, x1, y1):
#		'''Координаты в долях. (0;0) -- левый нижний угол 'холста'.
#		(1;1) -- правый верхний угол 'холста'.'''
#	def text(self, x, y, align, text)

class BG_HtmlCanvas(BG_CanvasBase):
	def __init__(self, size_x, size_y):
		self.__canvas  = html.CANVAS(width=size_x, height=size_y)
		self.__context = self.__canvas.getContext('2d')

		self.size_x = size_x
		self.size_y = size_y

	def fit(self):
		x = window.innerWidth  - self.get().getBoundingClientRect().left  - 16 -200
		y = window.innerHeight - self.get().getBoundingClientRect().top   - 16
		window.resizeCanvas(self.__context, x, y)
		self.size_x = x
		self.size_y = y

	def get(self):
		return self.__canvas

	def clear(self):
		self.__context.clearRect(0, 0, self.size_x, self.size_y)

	def X(self, x): return round(x*self.size_x)
	def Y(self, y): return round(self.size_y*(1-y))

	def line(self, a, b):
		c = self.__context

		c.beginPath()
		c.moveTo(self.X(a[0]), self.Y(a[1]))
		c.lineTo(self.X(b[0]), self.Y(b[1]))
		c.stroke()

	def text(self, a, align, text):
		if   align == self.LEFT  : self.__context.textAlign = 'left';   self.__context.textBaseline = 'middle'
		elif align == self.BOTTOM: self.__context.textAlign = 'center'; self.__context.textBaseline = 'bottom'
		elif align == self.RIGHT : self.__context.textAlign = 'right';  self.__context.textBaseline = 'middle'
		elif align == self.TOP   : self.__context.textAlign = 'center'; self.__context.textBaseline = 'top'
		else:
			raise Exception()
		self.__context.fillStyle = '#000'
		self.__context.fillText(str(text), self.X(a[0]), self.Y(a[1]))
#class BG_HtmlCanvas(BG_CanvasBase):

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

	def base(x_min, y_min, x_max, y_max):
		BG_Item._x_min = x_min
		BG_Item._y_min = y_min

		BG_Item._x_max = x_max
		BG_Item._y_max = y_max

	def dashes(mi, ma):
		if mi == None or ma == None:
			return None, ()
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
		return map(lambda i: f*i, range(g, h+1))

	def _dashes_log(mi, ma):
		a = ceil(log(mi, 10))
		b = ceil(log(ma, 10))
		return map(lambda i: 10**i, range(a, b))

	def _linear(mi, x, ma): return (x-mi)/(ma-mi)
	def _log(mi, y, ma):    return log(y/mi)/log(ma/mi)

	def _affinis(x, y, tg):
		if    0   <= tg <= 0.5:
			# x = x
			y = y*(1-tg)+x*tg
		elif -0.5 <= tg <  0:
			# x = x
			y = y*(1+tg)-tg+x*tg
		else:
			raise Exception()
		return x, y

	def _compress(x, y):
		x_min, y_min, x_max, y_max = 0.1, 0.1, 0.9, 0.9

		x = x_min + x*(x_max-x_min)
		y = y_min + y*(y_max-y_min)

		return x, y

	def point(x, y):
		x = BG_Item._linear(BG_Item._x_min, x, BG_Item._x_max)
		if BG_Item._logY == False:
			y = BG_Item._linear(BG_Item._y_min, y, BG_Item._y_max)
		else:
			y = BG_Item._log   (BG_Item._y_min, y, BG_Item._y_max)

		if BG_Item._affinisTg != None:
			x, y = BG_Item._affinis(x, y, BG_Item._affinisTg.tg())

		return BG_Item._compress(x, y)

	def setProp(prop):
		BG_Item._logY = False
		BG_Item._affinisTg = None
		BG_Item.dashes_y = BG_Item.dashes

		for i in flatten(prop):
			if   isinstance(i, BG_LogY):
				BG_Item._logY      = True
				BG_Item.dashes_y   = BG_Item._dashes_log
			elif isinstance(i, BG_Affinis):
				BG_Item._affinisTg = i
			else:
				raise Exception()
#class BG_Item:

class BG_Space(BG_Item):
	def __init__(self, x_min, y_min, x_max, y_max):
		self._x_min = x_min
		self._y_min = y_min
		self._x_max = x_max
		self._y_max = y_max

	def draw(self, canvas, x_min, y_min, x_max, y_max):
		pass

	def getSize(self):
		return (self._x_min,
		        self._y_min,
		        self._x_max,
		        self._y_max)

class BG_Frame(BG_Item):
	def draw(self, canvas, x_min, y_min, x_max, y_max):
		canvas.line(BG_Item.point(x_min, y_min), BG_Item.point(x_min, y_max))
		canvas.line(BG_Item.point(x_min, y_max), BG_Item.point(x_max, y_max))
		canvas.line(BG_Item.point(x_max, y_max), BG_Item.point(x_max, y_min))
		canvas.line(BG_Item.point(x_max, y_min), BG_Item.point(x_min, y_min))

		for x in BG_Frame.dashes(x_min, x_max):
			a = BG_Item.point(x, y_max)
			b = (a[0], a[1]+0.02)
			c = BG_Item.point(x, y_min)
			d = (c[0], c[1]-0.02)
			canvas.line(a, b)          # верхняя
			canvas.line(c, d)          # нижняя
			if x%5 == 0:
				canvas.text(b, BG_CanvasBase.BOTTOM,  x)
				canvas.text(d, BG_CanvasBase.TOP,     x)

		for y in BG_Item.dashes_y(y_min, y_max):
			a = BG_Item.point(x_min, y)
			b = (a[0]-0.02, a[1])
			c = BG_Item.point(x_max, y)
			d = (c[0]+0.02, c[1])
			canvas.line(a, b)     # левая
			canvas.line(c, d)     # правая
			canvas.text(b, BG_CanvasBase.RIGHT, y)
			canvas.text(d, BG_CanvasBase.LEFT,  y)

	def getSize(self):
		return None, None, None, None
#class BG_Frame(BG_Item):

class BG_Grid(BG_Item):
	def draw(self, canvas, x_min, y_min, x_max, y_max):
		for x in BG_Frame.dashes(x_min, x_max):
			a = BG_Item.point(x, y_min)
			b = BG_Item.point(x, y_max)
			canvas.line(a, b)

		for y in BG_Item.dashes_y(y_min, y_max):
			a = BG_Item.point(x_min, y)
			b = BG_Item.point(x_max, y)
			canvas.line(a, b)

	def getSize(self):
		return None, None, None, None

class BG_BubbleLevel(BG_Item):
	def __init__(self, n):
		self._n = n

	def draw(self, canvas, x_min, y_min, x_max, y_max):
		for i in range(self._n):
			y = (1/self._n)*(i+0.5)
			canvas.line((0, y), (1, y))

	def getSize(self):
		return None, None, None, None

class BG_TableFunc(BG_Item):
	def __init__(self, xy):
		'''Координаты математики'''
		self._data = tuple(xy)

		if len(self._data) == 0:
			self._x_min = None
			self._x_max = None
			self._y_min = None
			self._y_max = None

			return

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
			BG_Item.base(x_min, y_min, x_max, y_max)
			canvas.line(BG_Item.point(x0, y0),
			            BG_Item.point(x1, y1))
	def getSize(self):
		'''Минимальные и максимальные координаты для этого объекта'''
		return (self._x_min,
		        self._y_min,
		        self._x_max,
		        self._y_max)
#class BG_TableFunc(BG_Item):

class BG_Decart:
	def __min_max(self, x_min, y_min, x_max, y_max):
		if self._x_min == None or x_min != None and x_min < self._x_min        : self._x_min = x_min
		if self._x_max == None or x_max != None and         self._x_max < x_max: self._x_max = x_max

		if self._y_min == None or y_min != None and y_min < self._y_min        : self._y_min = y_min
		if self._y_max == None or y_max != None and         self._y_max < y_max: self._y_max = y_max

	def __init__(self, canvas, prop, *args):
		self._canvas = canvas
		self._prop   = prop

		self._data = args

		self._x_min = None
		self._y_min = None
		self._x_max = None
		self._y_max = None

	def clear(self):
		self._canvas.clear()

	def setProp(self, prop):
		self._prop = prop
		BG_Item.setProp(self._prop)

	def draw(self, *args):
		a = tuple(flatten(args))
		BG_Item.setProp(self._prop)

		for i in a:
			b = i.getSize()
			self.__min_max(*b)

		BG_Item.base(self._x_min, self._y_min, self._x_max, self._y_max)

		for i in flatten(self._data, a):
			i.draw(self._canvas, self._x_min,
			                     self._y_min,
			                     self._x_max,
			                     self._y_max)

	def redraw(self, *args):
		self.clear()

		self._x_min = None
		self._y_min = None
		self._x_max = None
		self._y_max = None

		self.draw(*args)
#class BG_Decart:
