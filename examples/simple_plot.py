# -*- coding: utf-8 -*-


import pyplotbrain as ppb
import pyqtgraph as pg
import numpy as np

app = pg.mkQApp()


view = ppb.addView(with_config = True)


colors = [ (1,0,0,.8), 
                (0,1,0,.8), 
                (0,0,1,.8),
                ]

for color in colors:
    
    n = 30
    
    node_coords = np.random.randn(n, 3)*20
    view.add_node(node_coords, color = color, size = 4)

    edge_width = np.zeros((n,n))
    edge_width[1,2] = 2
    edge_width[4,7] = 5
    edge_width[5,2] = 6
    
    view.add_edge(node_coords, width =3, color = color)


app.exec_()



