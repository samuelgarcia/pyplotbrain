# -*- coding: utf-8 -*-

import os
import numpy as np
from collections import OrderedDict


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
        faces = read_n_lines(f, nline,ncols = 3, dtype = int, sep = ' ')-1
    return coords, faces
    



p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meshdata')
cortical_meshes = OrderedDict()
for filename in os.listdir(p):
    k = filename.replace('.nv', '')
    cortical_meshes[k] = read_mesh(os.path.join(p, filename))
    

def test_read_mesh():
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meshdata/BrainMesh_ICBM152.nv')
    coords, faces = read_mesh(filename)
    
if __name__ == '__main__':
    test_read_mesh()


