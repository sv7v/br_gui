'''
Project 'Browser GUI for Brython' (BG)
См.:
-  https://brython.info/
-  https://t.me/olympgeom/568
   https://paolini.github.io/rosette/
-  https://stackoverflow.com/questions/53427699/editing-selections-of-path-points-or-line
   https://ru.stackoverflow.com/questions/1099795/Редактирование-выбора-точек-пути-или-линии
'''
from browser    import *
from pair_iterator  import *
from browser        import svg

from math           import *
from itertools      import *
from io             import StringIO

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

class BG_Html:
	def inline(self): self._data.style.display = 'inline'
	def none(self):   self._data.style.display = 'none'

	def show(self, show=True):
		if show: self.inline()
		else:    self.none()

	def __le__(self, other):
		try:
			self._data <= other.get()
		except AttributeError:
			self._data <= other

	def get(self):
		return self._data

class BG_Div(BG_Html):
	def __init__(self):
		self._data = html.DIV()

	def setText(self, text):
		self._data.text = str(text)

class BG_LocalTextFile(BG_Html):
	def __init__(self, callback):
		def readlines(s):
			with StringIO(s) as f:
				return f.readlines()

		self._data = html.INPUT(type='file')
		def input(event):
			file = self._data.files[0]

			reader = window.FileReader.new()
			reader.readAsText(file)
			reader.bind('load', lambda event: callback(readlines(event.target.result)))

		self._data.bind('input', input)
#class BG_LocalTextFile:

class BG_CheckBox(BG_Html):
	def __init__(self, title=None):
		self._data = html.INPUT(type='checkbox')
		if title != None:
			self._data['title'] = str(title)

	def setCallback(self, callback):
		self._callback = callback
		self._data.bind('change', lambda event: self._callback(event.target.checked))

	def getState(self):
		return self._data.checked

	def set(self, state=True):
		self._data.checked = state

class BG_Range(BG_Html):
	def __init__(self, callback):
		self._data = html.INPUT(type  = 'range',
		                        style = 'transform: rotate(-90deg); transform-origin: 0px 0px;',
		                        min   = '-50',
		                        max   = '50',
		                        value = '0')
		def hook(event):
			return callback(float(event.target.value) / 100)
#
		self._data.bind('change', hook)
#		self._data.bind('input''  hook)

	def getState(self):
		return float(self._data.value) / 100

class BG_CanvasBase(BG_Html):
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
		self._data     = html.CANVAS(width=size_x, height=size_y)
		self.__context = self._data.getContext('2d')

		self._size_x = size_x
		self._size_y = size_y

	def fit(self):
		x = window.innerWidth  - self.get().getBoundingClientRect().left  - 16 -200
		y = window.innerHeight - self.get().getBoundingClientRect().top   - 12
		window.resizeCanvas(self.__context, x, y)
		self._size_x = x
		self._size_y = y

	def getSize(self):
		return (self._size_x,
		        self._size_y)

	def mouseover(self, callback):
		self._data.bind('mousemove', lambda event: callback(event.offsetX+0.5,
		                                                    self._size_y - (event.offsetY+0.5),
		                                                    event.offsetX/(self._size_x-1),
		                                                    event.offsetY/(self._size_y-1)))

	def clear(self):
		self.__context.clearRect(0, 0, self._size_x, self._size_y)

	def X(self, x): return round(x * (self._size_x-1))      +0.5
	def Y(self, y): return round((self._size_y-1) * (1-y))  +0.5

	def line0(self, a, b):
		c = self.__context

		c.beginPath()
		c.moveTo(a[0], self._size_y - a[1])
		c.lineTo(b[0], self._size_y - b[1])
		c.stroke()

	def line(self, a, b):
		x0 = self.X(a[0])
		y0 = self.Y(a[1])
		x1 = self.X(b[0])
		y1 = self.Y(b[1])
		if (x0, y0) == (x1, y1):
			return

		c = self.__context
		self.line0((x0, self._size_y - y0), (x1, self._size_y - y1))

	def text(self, a, align, text):
		if   align == self.LEFT  : self.__context.textAlign = 'left';   self.__context.textBaseline = 'middle'
		elif align == self.BOTTOM: self.__context.textAlign = 'center'; self.__context.textBaseline = 'bottom'
		elif align == self.RIGHT : self.__context.textAlign = 'right';  self.__context.textBaseline = 'middle'
		elif align == self.TOP   : self.__context.textAlign = 'center'; self.__context.textBaseline = 'top'
		else:
			raise Exception()
		self.__context.fillStyle = '#000'
		self.__context.fillText(str(text), self.X(a[0]), self.Y(a[1]))

	def getRect(self, x, y, size_x, size_y):
		s_x = size_x
		s_y = size_y

		if s_x == 0 : s_x = 1
		if s_y == 0 : s_y = 1

		return self.__context.getImageData(x,
		                                   self._size_y - y,
		                                   s_x,
		                                   s_y)

	def putRect(self, data, x, y):
		self.__context.putImageData(data, x, self._size_y - y)
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

class BG_Property:
	def base(x_min, y_min, x_max, y_max):
		BG_Property._x_min = x_min;
		BG_Property._y_min = y_min;
		BG_Property._x_max = x_max;
		BG_Property._y_max = y_max;

	def convert(self, x, y):
		return self.conv_x(x), self.conv_y(y)

	def revers(self, x, y):
		return self.rev_x(x), self.rev_y(y)

class BG_Liner(BG_Property):
	# min max
	#  0   1
	def __init__(self):
		def linear(mi, a, ma):    return (a-mi)/(ma-mi)

		self.conv_x = lambda a: linear(BG_Property._x_min, a, BG_Property._x_max)
		self.conv_y = lambda a: linear(BG_Property._y_min, a, BG_Property._y_max)

		def liner_rev(mi, a, ma):
			return mi + a*(ma-mi)

		self.rev_x  = lambda a: liner_rev(BG_Property._x_min, a, BG_Property._x_max)
		self.rev_y  = lambda a: liner_rev(BG_Property._y_min, a, BG_Property._y_max)

class BG_LogY(BG_Liner):
	def __init__(self):
		super().__init__()
		def l(mi, y, ma):     return log(y/mi)/log(ma/mi)

		self.conv_y = lambda y: l    (BG_Property._y_min, y, BG_Property._y_max)

		def l_rev(mi, y, ma): return mi * exp(y*log(ma/mi))

		self.rev_y = lambda y:  l_rev(BG_Property._y_min, y, BG_Property._y_max)

class BG_Affinis(BG_Property):
	def __init__(self, tg=0):
		self._tg = tg

	def convert(self, x, y):
		tg = self._tg
		if    0   <= tg <= 0.5:
			# x = x
			y = y*(1-tg)+x*tg
		elif -0.5 <= tg <  0:
			# x = x
			y = y*(1+tg)-tg+x*tg
		else:
			raise Exception()
		return x, y

	def revers(self, x, y):
		tg = self._tg
		if    0   <= tg <= 0.5:
			# x = x
			y = (y-x*tg)/(1-tg)
		elif -0.5 <= tg <  0:
			# x = x
			y = (y+tg-x*tg)/(1+tg)
		else:
			raise Exception()
		return x, y


class BG_Compress(BG_Property):
	# 0   1        0   1
	# 0.1 0.9     mi  ma
	def __init__(self):
		mi = 0.1
		ma = 0.9

		def conv(x): return mi + x*(ma-mi)
		def rev(x):  return (x-mi)/(ma-mi)

		self.conv_x = conv
		self.conv_y = conv

		self.rev_x  = rev
		self.rev_y  = rev

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

		BG_Property.base(x_min, y_min, x_max, y_max)

	def getSize(self):
		return None, None, None, None

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

	def dashes_y(mi, ma):
		if not BG_LogY in BG_Item._prop:
			return BG_Item.dashes(mi, ma)
		else:
			return BG_Item._dashes_log(mi, ma)

	def point(x, y):
		try:
			x, y = BG_Item._prop[BG_LogY].convert(x, y)
		except KeyError:
			x, y = BG_Liner().convert(x, y)

		x, y = BG_Item._prop[BG_Affinis].convert(x, y)
		return BG_Compress().convert(x, y)

	def revers(x, y):
		y = 1 - y
		x, y = BG_Compress().revers(x, y)
		x, y = BG_Item._prop[BG_Affinis].revers(x, y)
		try:
			x, y = BG_Item._prop[BG_LogY].revers(x, y)
		except KeyError:
			x, y = BG_Liner().revers(x, y)
		return x, y

	def setProp(prop):
		try:
			BG_Item._prop
		except AttributeError:
			BG_Item._prop = dict()

		for i in flatten(prop):
			BG_Item._prop[type(i)] = i

			if type(i) == BG_Liner: BG_Item.delProp(BG_LogY())
			if type(i) == BG_LogY:  BG_Item.delProp(BG_Liner())

	def delProp(prop):
		try:
			del BG_Item._prop[type(prop)]
		except KeyError:
			pass
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

class BG_BubbleLevel(BG_Item):
	def __init__(self, n):
		self._n = n

	def draw(self, canvas, x_min, y_min, x_max, y_max):
		for i in range(self._n):
			y = (1/self._n)*(i+0.5)
			canvas.line((0, y), (1, y))

class BG_Tool:
	pass

class BG_VerticalRooler(BG_Tool):
	def __init__(self, decart):
		self._decart = decart
		self._x      = None
		self._data   = None
		self._size_y = decart.getSize()[1]

	def mouseover(self, dot_x, x):
		if self._x != None:
			self._clear()
		self._x = dot_x
		self._draw()

	def _clear(self):
		self._decart.putRect(self._data, round(self._x-0.5), self._size_y)

	def _draw(self):
		self._data = self._decart.getRect(round(self._x-0.5), self._size_y, 1, self._size_y)
		self._decart.line0((self._x, 0.5), (self._x, round(self._size_y - 0.5)))

class BG_LeftRightBorder(BG_Tool):
	def __init__(self, decart):
		self._decart = decart

		left, bottom, right, top = decart.getMinMax()

		self._left  = decart.dot(left, bottom)[0]
		self._right = decart.dot(right, top)[0]

	def mouseover(self, dot_x, x):
		if   abs(dot_x - self._left) <=3 :
			self._decart.get().style.cursor = 'w-resize'
		elif abs(dot_x - self._right) <= 3:
			self._decart.get().style.cursor = 'e-resize'
		else:
			self._decart.get().style.cursor = 'default'

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
		BG_Item.base(x_min, y_min, x_max, y_max)
		for (x0,y0),(x1,y1) in pair(self._data):
			canvas.line(BG_Item.point(x0, y0),
			            BG_Item.point(x1, y1))
	def getSize(self):
		'''Минимальные и максимальные координаты для этого объекта'''
		return (self._x_min,
		        self._y_min,
		        self._x_max,
		        self._y_max)
#class BG_TableFunc(BG_Item):

class BG_Decart(BG_HtmlCanvas):
	def __min_max(self, x_min, y_min, x_max, y_max):
		if self._x_min == None or x_min != None and x_min < self._x_min        : self._x_min = x_min
		if self._x_max == None or x_max != None and         self._x_max < x_max: self._x_max = x_max

		if self._y_min == None or y_min != None and y_min < self._y_min        : self._y_min = y_min
		if self._y_max == None or y_max != None and         self._y_max < y_max: self._y_max = y_max

	def __init__(self):
		super().__init__(1,1)

		self._x_min = None
		self._y_min = None
		self._x_max = None
		self._y_max = None

		self._funcs = []

	def mouseover(self, callback):
		super().mouseover(lambda dot_x, dot_y, x, y:
		                  callback(dot_x, dot_y, *BG_Item.revers(x, y)))

	def setProp(self, *prop):
		self._prop = prop
		BG_Item.setProp(self._prop)

	def delProp(self, *prop):
		for i in flatten(prop):
			BG_Item.delProp(i)

	def setRooler(self, *rooler):
		self._rooler = rooler

	def draw(self, *funcs):
		self._funcs.append(funcs)
		self.redraw()

	def redraw(self):
		self._x_min = None
		self._y_min = None
		self._x_max = None
		self._y_max = None

		funcs = tuple(flatten(self._funcs))

		if 0 == len(funcs):
			return

		for i in funcs:
			b = i.getSize()
			self.__min_max(*b)

		BG_Item.base(self._x_min, self._y_min, self._x_max, self._y_max)

		self.clear()
		for i in flatten(self._rooler, funcs):
			i.draw(self, self._x_min,
			             self._y_min,
			             self._x_max,
			             self._y_max)
	def getMinMax(self):
		return (self._x_min,
		        self._y_min,
		        self._x_max,
		        self._y_max)

	def dot(self, x, y):
		a, b = BG_Item.point(x, y)
		return (self.X(a),
		        self.Y(b))
#class BG_Decart(BG_HtmlCanvas):
