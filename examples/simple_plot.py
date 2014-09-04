# -*- coding: utf-8 -*-


import pyplotbrain as ppb
import pyqtgraph as pg
import numpy as np

app = pg.mkQApp()


view = ppb.addView(with_config = True,
                background_color = 'k',
                cortical_mesh = 'BrainMesh_ICBM152',
                cortical_alpha = .6,
                cortical_color = 'w',
                )


colors = [ (1,0,0,.8), 
                (0,1,0,.8), 
                (0,0,1,.8),
                ]

for color in colors:
    
    n = 30
    
    node_coords = np.random.randn(n, 3)*20
    view.add_node(node_coords, color = color, size = 4)

    connection_with = np.zeros((n,n))
    connection_with[1,2] = 3
    connection_with[4,7] = 5
    connection_with[5,2] = 6
    connection_with[8,5] = 4.5
    connection_with[2,4] = 6
    connection_with[8,2] = 6
    
    view.add_edge(node_coords,connection_with,color = color)

view.to_file('test1.png')
view.to_file('test2.jpg')

app.exec_()



