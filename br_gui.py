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
