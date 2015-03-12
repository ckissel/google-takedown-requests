import logging
logging.basicConfig(level=logging.DEBUG)

import numpy as np

from CDSBuilder import buildsource

from bokeh.plotting import figure
from bokeh.models import Plot, ColumnDataSource, HoverTool
from bokeh.properties import Instance
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.models.widgets import HBox, Slider, TextInput, VBoxForm

#TEST DATA
class entity:
    'entity objects'
    def __init__(self,name,category,size):
        self.name=name
        self.category=category
        self.size=size
        self.x=None
        self.y=None
        self.width=1
        self.alpha=1
class Display_Entity:
    'display entity'
    def __init__(self,center,outer):
        self.center=center
        self.outer=outer
fox=entity("fox","requester",20)
cnn=entity("cnn","requester",30)
bbc=entity("bbc","requester",15)

steve=entity("steve","target",21)

DE=Display_Entity(steve,[fox,cnn,bbc])

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

		obj.line_height = Slider(title="line_height", name="line_height", value=1.0, start=0.0, end=5.0, step=0.1)

		# plot = figure(plot_height=400, plot_width=400, title='herpderp', x_range=[0, 5], y_range=[0, 5])
		plot = figure(title="Takedown Visualization for ", tools="hover", x_range=[-50,50], y_range=[-50,50], plot_width=800, plot_height=800)

		plot.grid.grid_line_color = None
		plot.axis.axis_line_color = None
		plot.axis.major_tick_line_color = None
		plot.axis.major_label_text_font_size = "0pt"



		# plot.line('x', 'y', source=obj.source, line_width=3)
		
		#build line web lists
		def joinit(iterable, delimiter):
			result=[]
			for item in iterable:
				result.append(item)
				result.append(delimiter)
			return result
		linex=joinit(obj.source.data['xcoords'],0.0)
		liney=joinit(obj.source.data['ycoords'],0.0)

		plot.line(x=linex,y=liney,line_width=1)

		plot.circle(source=obj.source, x='xcoords', y='ycoords', color='colors', size='sizes')

		#Tooltips
		hover = plot.select(dict(type=HoverTool))
		hover.tooltips = [
		('Name','@names'),
		('Amount','@widths'),
		('Failure Rate', '@alphas')
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
		N = 200

		v = self.line_height.value  # the current value of the line height slider

		x = np.linspace(0, 5, N)
		y = np.linspace(v, v, N)

		# self.source.data = dict(x=x, y=y)
		self.source = buildsource(DE)[0]

@bokeh_app.route('/bokeh/sliders/')
@object_page("sin")
def make_slider():
	app = TestSliderApp.create()
	return app