#test script 3_5
#This should draw a sample screen

from bokeh.plotting import figure, output_file, show


output_file("test.html")

p=figure(background_fill="white",border_fill='green',min_border=0,title="ELECTRIC DICKBUTT EXPRESS",x_range=[-100,100],y_range=[-100,100],plot_width=400, plot_height=400)
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_label_text_font_size = "0pt"
p.axis.major_label_standoff = 0
p.circle([0], [0],
         size=40, # px
         fill_alpha=0.5,
         fill_color="steelblue",
         line_alpha=0.8,
         line_color="crimson")



show(p)