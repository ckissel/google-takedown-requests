#This function takes a DE and builds a Column Data Source

import numpy as np

from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource



def genpositions(n,r): #takes in a number of positions to be generated
    
    return map(list, zip(*[(np.cos(2*np.pi/n*x)*r,np.sin(2*np.pi/n*x)*r) for x in xrange(0,n+1)]))

def buildsource(DE):
    
    items=len(DE.outer)
    maxsize=max(max(entity.size) for entity in DE.outer)
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

    # max_size = max([ent.size[0] for ent in DE.outer])
    # min_size = min([ent.size[0] for ent in DE.outer])
    # norm_range = max_size - min_size
    # print "LOOK AT ME", max_size, min_size, norm_range

    #populate list from objects
    for entity in DE.outer:
        names.append(entity.name)
        xcoords.append(entity.x)
        ycoords.append(entity.y)
        if entity.category == 'requester':
            colors.append('blue')
        if entity.category == 'target':
            colors.append('orange')
        sizes.append(int(np.sqrt(entity.size[0])))
    #do it for the center too:
    # names.append(DE.center.name)
    # xcoords.append(DE.center.x)
    # ycoords.append(DE.center.y)
    # if DE.center.category == 'requester':
    #     colors.append('blue')
    # if DE.center.category == 'target':
    #     colors.append('orange')
    # sizes.append(DE.center.size)


    
    source = ColumnDataSource(
        data=dict(
            names=names,
            xcoords=xcoords,
            ycoords=ycoords,
            colors=colors,
            sizes=sizes,
            # widths=[entity.width for entity in DE.outer],
            # alphas=[entity.alpha for entity in DE.outer]
        )
    )
    x_range=[min(xcoords)-maxsize-5,max(xcoords)+maxsize+5] 
    y_range=[min(ycoords)-maxsize-5,max(ycoords)+maxsize+5]
    return source, x_range, y_range