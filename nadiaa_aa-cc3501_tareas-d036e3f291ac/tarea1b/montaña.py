import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


def createMontana():

    gpuGreenTr = es.toGPUShape(bs.createColorTriangle(0.6275, 0.3137, 0))

    #Se crea la figura basica que es una sola montaña 
    montana = sg.SceneGraphNode("montana")
    montana.translate = tr.scale(1.6,0.3,0)
    montana.childs = [gpuGreenTr]

    return montana

def createMontanas(N):

    montanas = sg.SceneGraphNode("montanas")

    baseName = "montana"
    for i in range(-N,N): #Se crea la fila de montañas
        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode.transform = tr.translate(0.4 * i, 0.5,0)
        newNode.childs += [createMontana()]

        montanas.childs +=  [newNode]

    return montanas


