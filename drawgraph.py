#test script 3_5
#This should draw a sample screen
import numpy as np

from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource



def genpositions(n,r): #takes in a number of positions to be generated
    
    return map(list, zip(*[(np.cos(2*np.pi/n*x)*r,np.sin(2*np.pi/n*x)*r) for x in xrange(0,n+1)]))

def drawgraph(DE):
    
    items=len(DE.outer)
    maxsize=max(entity.size for entity in DE.outer)
    r=((maxsize*2*1.1)*items)/(2*np.pi) #radius is circle diameter + breathing room times amount of items/2pi
    points=genpositions(items,r)
    xs=points[0]
    ys=points[1]
    #assign each object coordinates
    for i, entity in enumerate(DE.outer):
        entity.x=xs[i]
        entity.y=ys[i]
    #place the center object at 0,0
    DE.center.x=0
    DE.center.y=0

    #build list of information
    names=[]
    xcoords=[]
    ycoords=[]
    colors=[]
    sizes=[]
    #populate list from objects
    for entity in DE.outer:
        names.append(entity.name)
        xcoords.append(entity.x)
        ycoords.append(entity.y)
        if entity.category == 'requester':
            colors.append('blue')
        if entity.category == 'target':
            colors.append('orange')
        sizes.append(entity.size)
    #do it for the center too:
    names.append(DE.center.name)
    xcoords.append(DE.center.x)
    ycoords.append(DE.center.y)
    if DE.center.category == 'requester':
        colors.append('blue')
    if DE.center.category == 'target':
        colors.append('orange')
    sizes.append(DE.center.size)


    
    source = ColumnDataSource(
        data=dict(
            names=names,
            xcoords=xcoords,
            ycoords=ycoords,
            colors=colors,
            sizes=sizes
        )
    )


    #now to draw the circles out

    output_file("graph.html")

    p = figure(title="Takedown Visualization for " + DE.center.name,
           tools="hover",
           x_range=[min(xcoords)-maxsize-5,max(xcoords)+maxsize+5], 
           y_range=[min(ycoords)-maxsize-5,max(ycoords)+maxsize+5], 
           plot_width=800, plot_height=800
           )

    p.circle(source=source, x=xcoords, y=ycoords, color=colors, size=sizes)


    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "0pt"

    hover = p.select(dict(category=HoverTool))
    hover.tooltips = [
        ('name'),
        ]


    show(p)

if __name__ == '__main__':
    class entity:
        'entity objects'
        def __init__(self,name,category,size):
            self.name=name
            self.category=category
            self.size=size
            x=None
            y=None
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
    drawgraph(DE)