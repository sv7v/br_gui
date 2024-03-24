'''
Project 'Browser GUI for Brython' (BG)
'''
from browser    import *

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
