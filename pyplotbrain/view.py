# -*- coding: utf-8 -*-

import numpy as np
import os

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.parametertree import Parameter, ParameterTree

from .plotmesh import cortical_meshes

from OpenGL.GL import glClearColor, glClear,GL_DEPTH_BUFFER_BIT, GL_COLOR_BUFFER_BIT


class View(QtGui.QWidget):
    def __init__(self, parent = None, with_config = False, **kargs ):
        QtGui.QWidget.__init__(self, parent)
        
        self.resize(800,600)
        
        mainlayout = QtGui.QVBoxLayout()
        self.setLayout(mainlayout)
        
        self.glview = gl.GLViewWidget()
        mainlayout.addWidget(self.glview)
        self.glview .setCameraPosition(160,160,15)
        
        
        if with_config:
            h = QtGui.QHBoxLayout()
            mainlayout.addLayout(h)
            but =  QtGui.QPushButton('Config', icon = QtGui.QIcon.fromTheme('configure'))
            h.addWidget(but)
            but.clicked.connect(self.open_params)
            but =  QtGui.QPushButton('Save png', icon = QtGui.QIcon.fromTheme('save'))
            h.addWidget(but)
            but.clicked.connect(self.open_save_dialog)
            
        
        
        _params = [
                {'name': 'cortical_mesh', 'type': 'list', 'values': cortical_meshes.keys(), 'value' :  'BrainMesh_ICBM152'},
                {'name': 'cortical_alpha', 'type': 'float', 'value': .1, 'limits': [0., 1.], 'step' : .01},
                {'name': 'cortical_color', 'type': 'color', 'value':  'w'},
                {'name': 'background_color', 'type': 'color', 'value':  'k'},
            ]
        self.params = Parameter.create(name='params', type='group', children=_params)
        self.tree = ParameterTree(parent = self)
        self.tree.setParameters(self.params)
        self.tree.setWindowFlags(QtCore.Qt.Dialog)
        
        
        
        self.mesh = None
        for k,v in kargs.items():
            self.params[k] = v
        self.change_background_color()
        self.plot_mesh()
        self.change_color_mesh()

        self.params.param('cortical_mesh').sigValueChanged.connect(self.plot_mesh)
        self.params.param('cortical_alpha').sigValueChanged.connect(self.change_color_mesh)
        self.params.param('cortical_color').sigValueChanged.connect(self.change_color_mesh)
        self.params.param('background_color').sigValueChanged.connect(self.change_background_color)

        self.glview.resizeGL(self.glview.width(), self.glview.height())

    def open_params(self):
        self.tree.show()
    
    def change_background_color(self):
        background_color =  self.params['background_color']
        try:
            self.glview.setBackgroundColor(background_color)
        except:
            #~ #FIXME this is buggy in pyqtgrap0.9.8
            bgcolor = pg.mkColor(QtGui.QColor(background_color))
            glClearColor(bgcolor.red()/255., bgcolor.green()/255., bgcolor.blue()/255., 1.0)
            glClear( GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT )
            self.glview.paintGL()
            self.glview.update()
    
    
    def plot_mesh(self):
        vertexes, faces = cortical_meshes[self.params['cortical_mesh']]
        alpha =  self.params['cortical_alpha']
        c = self.params['cortical_color']
        color = (c.red()/255., c.green()/255.,c.blue()/255.,alpha)
        if self.mesh is None:
            
            self.mesh = gl.GLMeshItem(vertexes=vertexes, faces=faces, smooth=True, drawFaces=True,
                                                    drawEdges=False,
                                                    edgeColor=(1.,1.,1.,.2), 
                                                    color = color,
                                                    computeNormals = False,
                                                    glOptions='translucent',
                                                    #~ glOptions='additive',
                                                    #~ shader='balloon',
                                                    shader='shaded', 
                                                    )
            self.glview.addItem(self.mesh)
        else:
            self.mesh.setMeshData(vertexes=vertexes, faces=faces)
            #~ self.mesh.set
            
    
    def change_color_mesh(self):
        alpha =  self.params['cortical_alpha']
        c = self.params['cortical_color']
        color = (c.red()/255., c.green()/255.,c.blue()/255.,alpha)
        self.mesh.setColor(color)
    
    def add_node(self, coords, color = (1,1,1,0), size = 5):
        sp1 = gl.GLScatterPlotItem(pos=coords, size=size, color=color, pxMode=False)
        self.glview.addItem(sp1)
    
    def add_edge(self, node_coords, connection_with, color = (1,1,1,1)):
        for i in range(node_coords.shape[0]):
            for j in range(node_coords.shape[1]):
                if connection_with[i,j] == 0: continue
                plt = gl.GLLinePlotItem(pos=np.vstack([node_coords[i], node_coords[j]]), color=color, width = connection_with[i,j])
                self.glview.addItem(plt)
    
    def open_save_dialog(self):
        text = u'Il est où mon côte du Rhône ?'
        QtGui.QMessageBox.warning(self,u'Fail',text,
                    QtGui.QMessageBox.Ok , QtGui.QMessageBox.NoButton)
        pathname =  unicode(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.DesktopLocation))
        filename = os.path.join(pathname, 'Il est beau le cerveau.png')
        filename = QtGui.QFileDialog.getSaveFileName( self, u'Save png',  filename, 'PNG (*.png)')
        if filename:
            self.to_file( filename)
    
    def to_file(self, filename):
        self.glview.readQImage().save(filename)
    


def addView(**kargs):
    view =  View(**kargs)
    view.show()
    return view



