#test script 3_5
#This should draw a sample screen
import math
from bokeh.plotting import figure, output_file, show



def genpositions(n,r): #takes in a number of positions to be generated
	
	return map(list, zip(*[(math.cos(2*math.pi/n*x)*r,math.sin(2*math.pi/n*x)*r) for x in xrange(0,n+1)]))

def drawgraph(items, maxcircle, title, names, sizes, centername, centersize):
	
	"""items=number of circles
	maxcircle=radius of the largest circle
	title=desired title of plot
	names=names of the circles, as a list
	sizes=radii of the circles, as a list
	centername=name of the circle in the middle
	centersize=size of center circle"""

	r=((maxcircle*2*1.1)*items)/(2*math.pi) #radius is circle diameter + breathing room times amount of items/2pi
	points=genpositions(items,r)
	xs=points[0]
	ys=points[1]
	
	#now to draw the circles out

	output_file("graph.html")

	p=figure(background_fill="white",
	border_fill='white',min_border=0,
	title=title,
	x_range=[-r-maxcircle,r+maxcircle],
	y_range=[-r-maxcircle,r+maxcircle],
	plot_width=800, plot_height=800)

	p.grid.grid_line_color = None
	p.axis.axis_line_color = None
	p.axis.major_label_text_font_size = "0pt"
	p.axis.major_label_standoff = 0
	p.circle(xs,ys,
    	    size=sizes, # px
        	fill_alpha=0.5,
         	fill_color="steelblue",
         	line_alpha=0.8,
         	line_color="crimson")
	#draw center circle
	p.circle([0],[0],size=centersize,fill_alpha=.8,fill_color="orange",line_alpha=.4,line_color="green")
	p.text([0],[0],centername,text_baseline="middle", text_align="center")

	#add text

	p.text(xs,ys,names,text_baseline="middle", text_align="center")

	show(p)

if __name__ == '__main__':
 	drawgraph(10,10,"magic Dickbutt partytime",['a','b','s','d','f','r','u','i','p','w'],[20,10,15,60,13,5,2,8,13,23],"Richard Keister",30)