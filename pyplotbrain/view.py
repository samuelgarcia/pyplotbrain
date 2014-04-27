# -*- coding: utf-8 -*-

import numpy as np

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.parametertree import Parameter, ParameterTree

from .plotmesh import cortical_meshes


class View(QtGui.QWidget):
    def __init__(self, parent = None, with_config = False, ):
        QtGui.QWidget.__init__(self, parent)
        
        self.resize(800,600)
        
        mainlayout = QtGui.QVBoxLayout()
        self.setLayout(mainlayout)
        
        self.glview = gl.GLViewWidget()
        mainlayout.addWidget(self.glview)
        self.glview .setCameraPosition(160,160,15)
        
        if with_config:
            but =  QtGui.QPushButton('Config', icon = QtGui.QIcon.fromTheme('configure'))
            mainlayout.addWidget(but)
            but.clicked.connect(self.open_params)
        
        
        _params = [
                {'name': 'cortical_mesh', 'type': 'list', 'values': cortical_meshes.keys()},
                {'name': 'cortical_alpha', 'type': 'float', 'value': .1, 'limits': [0., 1.], 'step' : .01},
            ]
        self.params = Parameter.create(name='params', type='group', children=_params)
        self.tree = ParameterTree(parent = self)
        self.tree.setParameters(self.params)
        self.tree.setWindowFlags(QtCore.Qt.Dialog)
        
        self.params.param('cortical_mesh').sigValueChanged.connect(self.plot_mesh)
        self.params.param('cortical_alpha').sigValueChanged.connect(self.change_alpha_mesh)
        
        
        self.mesh = None
        
        self.params['cortical_mesh'] =  'BrainMesh_ICBM152'
        
        
    def open_params(self):
        self.tree.show()
        
    def plot_mesh(self):
        vertexes, faces = cortical_meshes[self.params['cortical_mesh']]
        if self.mesh is None:
            alpha =  self.params['cortical_alpha']
            self.mesh = gl.GLMeshItem(vertexes=vertexes, faces=faces, smooth=True, drawFaces=True,
                                                    drawEdges=False,
                                                    edgeColor=(1,1,1,.2), 
                                                    color = (1,1,1,alpha),
                                                    computeNormals = False,
                                                    #~ glOptions='translucent',
                                                    glOptions='additive',
                                                    #~ shader='balloon',
                                                    #~ shader='shaded', 
                                                    )
            self.glview.addItem(self.mesh)
        else:
            self.mesh.setMeshData(vertexes=vertexes, faces=faces)
            #~ self.mesh.set
            
    
    def change_alpha_mesh(self):
        alpha =  self.params['cortical_alpha']
        color = self.mesh.opts['color']
        self.mesh.setColor(color[:3]+(alpha,))
    
    def add_node(self, coords, color = (1,1,1,0), size = 5):
        sp1 = gl.GLScatterPlotItem(pos=coords, size=size, color=color, pxMode=False)
        self.glview.addItem(sp1)
    
    def add_edge(self, node_coords, connection_with, color = (1,1,1,1)):
        for i in range(node_coords.shape[0]):
            for j in range(node_coords.shape[1]):
                if connection_with[i,j] == 0: continue
                plt = gl.GLLinePlotItem(pos=np.vstack([node_coords[i], node_coords[j]]), color=color, width = connection_with[i,j])
                self.glview.addItem(plt)
                


def addView(**kargs):
    view =  View(**kargs)
    view.show()
    return view



