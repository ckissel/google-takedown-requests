import numpy as np
from bokeh.document import Document
from bokeh.models import ColumnDataSource, DataRange1d, Plot, LinearAxis, Grid
from bokeh.models.glyphs import Text
from bokeh.plotting import show, output_file
output_file("graph.html")
N = 9
x = np.linspace(-2, 2, N)
print x
y = x
a = "abcdefghijklmnopqrstuvwxyz"
text = [a[i*3:i*3+3] for i in range(N)]
source = ColumnDataSource(dict(x=x, y=y, text=text))
xdr = DataRange1d(sources=[source.columns("x")])
ydr = DataRange1d(sources=[source.columns("y")])
plot = Plot(
title=None, x_range=xdr, y_range=ydr, plot_width=300, plot_height=300,
h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location=None)
glyph = Text(x="x", y="y", text="text", angle=0.3, text_color="#96deb3")
plot.add_glyph(source, glyph)
xaxis = LinearAxis()
plot.add_layout(xaxis, 'below')
yaxis = LinearAxis()
plot.add_layout(yaxis, 'left')
plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
doc = Document()
doc.add(plot)
show(plot)