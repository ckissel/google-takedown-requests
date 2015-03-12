import logging
logging.basicConfig(level=logging.DEBUG)

import numpy as np
from pandas import read_pickle
from data_utils import DisplayEntity

from CDSBuilder import buildsource

from bokeh.plotting import figure
from bokeh.models import Plot, ColumnDataSource, HoverTool
from bokeh.properties import Instance
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.models.widgets import HBox, Slider, TextInput, VBoxForm

#TEST DATA
# class entity:
#     'entity objects'
#     def __init__(self,name,category,size):
#         self.name=name
#         self.category=category
#         self.size=size
#         self.x=None
#         self.y=None
#         # self.width=1
#         # self.alpha=1
# class Display_Entity:
#     'display entity'
#     def __init__(self,center,outer):
#         self.center=center
#         self.outer=outer
# fox=entity("fox","requester",[20,10,2,40,21])
# cnn=entity("cnn","requester",[30,4,2,40,31])
# bbc=entity("bbc","requester",[15,14,20,90,2])

# steve=entity("steve","target",21)

DE=read_pickle('first_hundred.p')


class TestSliderApp(HBox):
	"""
	Our test app based on the bokeh slider app example.
	Inherits from HBox, whatever that is.
	It's going to change the height of a line!
	"""
	extra_generated_classes = [["TestSliderApp", "TestSliderApp", "HBox"]]

	# the form for our input (its children will be the actual inputs)
	inputs = Instance(VBoxForm)

	# make an instance of the Slider object
	line_height = Instance(Slider)

	# make the plot instance
	plot = Instance(Plot)

	# ugh
	source = Instance(ColumnDataSource)

	# I don't know why this is a class method
	@classmethod
	def create(cls):
		"""
		One-time creation of the app's objects.
		"""

		obj = cls()

		source, x_range, y_range = buildsource(DE)
		# obj.source = ColumnDataSource(data=dict(x=[], y=[]))
		obj.source = source
		print 'DICKBUTT', source.data

		obj.line_height = Slider(title="Request Type", name="line_height", value=0, start=0, end=1, step=1)

		# plot = figure(plot_height=400, plot_width=400, title='herpderp', x_range=[0, 5], y_range=[0, 5])
		plot = figure(title="Takedown Visualization for Fox (2014)", tools="hover,wheel_zoom", x_range=x_range, y_range=y_range, plot_width=800, plot_height=800)

		plot.grid.grid_line_color = None
		plot.axis.axis_line_color = None
		plot.axis.major_tick_line_color = None
		plot.axis.major_label_text_font_size = "0pt"



		# plot.line('x', 'y', source=obj.source, line_width=3)
		
		#build line web lists
		# def joinit(iterable, delimiter):
		# 	result=[]
		# 	for item in iterable:
		# 		result.append(item)
		# 		result.append(delimiter)
		# 	return result
		# linex=joinit(obj.source.data['xcoords'],0.0)
		# liney=joinit(obj.source.data['ycoords'],0.0)
		# linewidths=joinit(obj.source.data['widths'],0.0)

		linex=[]
		liney=[]
		for i in range(len(obj.source.data['xcoords'])):
			linex.append([0,obj.source.data['xcoords'][i]])
			liney.append([0,obj.source.data['ycoords'][i]])

		

		plot.multi_line(xs=linex, ys=liney, color='green')
		
		plot.circle(source=obj.source, x='xcoords', y='ycoords', color='colors', size='sizes')
		plot.circle(x=[0],y=[0],color='blue',size=30)

		#Tooltips
		hover = plot.select(dict(type=HoverTool))
		hover.tooltips = [
		('Name','@names'),
		('Take-Down Requests','@sizes'),
		('X-Coordinate', '@xcoords')
		]

		obj.plot = plot
		obj.update_data()

		obj.inputs = VBoxForm(children=[obj.line_height])

		# no idea why this is necessary
		obj.children.append(obj.inputs)
		obj.children.append(obj.plot)

		return obj

	def setup_events(self):
		"""
		Attaches the on_change event to the value property.
		"""

		property_name = 'value'
		callback_name = 'input_change'

		# what even
		super(TestSliderApp, self).setup_events()
		if not self.line_height:
			return
		self.line_height.on_change(property_name, self, callback_name)

	def input_change(self, obj, attrname, old, new):
		"""
		Executes whenever the slider is slid (i.e. "value" changes).
		"""

		
		self.update_data()

	def update_data(self):
		"""
		herpderp
		"""
		# N = 200

		v = self.line_height.value  # the current value of the line height slider

		# x = np.linspace(0, 5, N)
		# y = np.linspace(v, v, N)

		# self.source.data = dict(x=x, y=y)
		# source, x_range, y_range = buildsource(DE)
		newSize=[]
		for entity in DE.outer:
			newSize.append(int(np.sqrt(entity.size[v])))
		self.source.data = dict(names=self.source.data['names'],
			xcoords=self.source.data['xcoords'],
			ycoords=self.source.data['ycoords'],
			colors=self.source.data['colors'],
			sizes=newSize
			)
			# widths=newWidth,
			# alphas=self.source.data['alphas'])



@bokeh_app.route('/bokeh/sliders/')
@object_page("sin")
def make_slider():
	app = TestSliderApp.create()
	return app