import numpy as np
from pandas import read_pickle
from entities import DisplayEntity  # imported so the pickle file doesn't cry

from CDSBuilder import buildsource

from bokeh.plotting import figure
from bokeh.models import Plot, ColumnDataSource, HoverTool
from bokeh.properties import Instance
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.models.widgets import HBox, Slider, VBoxForm

# TEST DATA
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

# Unpickle the file containing a DisplayEntity object for the first hundred domains of the Fox data
DE = read_pickle('first_hundred.p')


class TestSliderApp(HBox):
    """
    Our test app based on the bokeh slider app example.
    All of this code is based on https://github.com/bokeh/bokeh/blob/master/examples/app/sliders_applet/sliders_app.py
    """
    extra_generated_classes = [["TestSliderApp", "TestSliderApp", "HBox"]]

    # the form for our input (its children will be the actual inputs)
    inputs = Instance(VBoxForm)

    # Slider object
    request_type = Instance(Slider)

    plot = Instance(Plot)

    # Data source for the plot
    source = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        """
        One-time creation of the app's objects.
        """

        obj = cls()

        # build a ColumnDataSource from the DisplayEntity object
        source, x_range, y_range = buildsource(DE)
        obj.source = source

        obj.request_type = Slider(title="Request Type", name="request_type", value=0, start=0, end=1, step=1)

        plot = figure(title="Takedown Visualization for Fox (2014)", tools="hover,wheel_zoom", x_range=x_range, y_range=y_range, plot_width=800, plot_height=800)

        plot.grid.grid_line_color = None
        plot.axis.axis_line_color = None
        plot.axis.major_tick_line_color = None
        plot.axis.major_label_text_font_size = "0pt"

        # build line web lists
        # def joinit(iterable, delimiter):
        #     result=[]
        #     for item in iterable:
        #         result.append(item)
        #         result.append(delimiter)
        #     return result
        # linex=joinit(obj.source.data['xcoords'],0.0)
        # liney=joinit(obj.source.data['ycoords'],0.0)
        # linewidths=joinit(obj.source.data['widths'],0.0)

        linex = []
        liney = []
        for i in range(len(obj.source.data['xcoords'])):
            linex.append([0, obj.source.data['xcoords'][i]])
            liney.append([0, obj.source.data['ycoords'][i]])

        plot.multi_line(xs=linex, ys=liney, color='green')

        plot.circle(source=obj.source, x='xcoords', y='ycoords', color='colors', size='sizes')
        plot.circle(x=[0], y=[0], color='blue', size=30)

        # Tooltips
        hover = plot.select(dict(type=HoverTool))
        hover.tooltips = [
            ('Name','@names'),
            ('Take-Down Requests','@numbers')
        ]

        obj.plot = plot
        obj.update_data()

        obj.inputs = VBoxForm(children=[obj.request_type])

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
        if not self.request_type:
            return
        self.request_type.on_change(property_name, self, callback_name)

    def input_change(self, obj, attrname, old, new):
        """
        Executes whenever the slider is slid (i.e. "value" changes).
        """
        self.update_data()

    def update_data(self):
        """
        Modify the ColumnDataSource that provides data to the view.
        """

        v = self.request_type.value  # the current value of the request type slider

        newSize = []
        numbers = []
        for entity in DE.outer:
            newSize.append(int(np.sqrt(entity.size[v])))
            numbers.append(entity.size[v])
        self.source.data = dict(names=self.source.data['names'],
            xcoords=self.source.data['xcoords'],
            ycoords=self.source.data['ycoords'],
            colors=self.source.data['colors'],
            sizes=newSize,
            numbers=numbers
        )
        # widths=newWidth,
        # alphas=self.source.data['alphas'])


@bokeh_app.route('/bokeh/sliders/')
@object_page("sin")
def make_slider():
    app = TestSliderApp.create()
    return app
