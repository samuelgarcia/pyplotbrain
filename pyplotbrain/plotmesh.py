# -*- coding: utf-8 -*-

import os
import numpy as np

def read_n_lines(f, nline,ncols = 3, dtype = float, sep = ' '):
    m = np.zeros((nline, ncols), dtype = dtype)
    for i in range(nline):
        line = f.readline()
        try:
            m[i,:] = [dtype(v)  for v in line.split(sep) ]
        except:
            print 'error', i, line
    return m


def read_mesh(filename):
    with open(filename)as f:
        nline =  int(f.readline())
        coords = read_n_lines(f, nline,ncols = 3, dtype = float, sep = ' ')
        nline =  int(f.readline())
        faces = read_n_lines(f, nline,ncols = 3, dtype = int, sep = ' ')
    return coords, faces-1
    
    
def test_read_mesh():
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meshdata/BrainMesh_ICBM152.nv')
    coords, faces = read_mesh(filename)
        
    from pyqtgraph.Qt import QtCore, QtGui
    import pyqtgraph as pg
    import pyqtgraph.opengl as gl
    import numpy as np



    app = QtGui.QApplication([])
    w = gl.GLViewWidget()
    w.show()



    #~ m1 = gl.GLMeshItem(vertexes=coords, faces=faces, smooth=True, drawFaces=False,  drawEdges=True, edgeColor=(1,1,1,.2), color = (.4,.4,.4,.3))
    m1 = gl.GLMeshItem(vertexes=coords, faces=faces, smooth=True, drawFaces=True,  drawEdges=False, edgeColor=(1,1,1,.2), color = (1,1,1,.1))
    m1.setGLOptions('additive')
    w.addItem(m1)
    
    app.exec_()
    
    
    
    
if __name__ == '__main__':
    test_read_mesh()
