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


def crearArbol():

    #Se crean las figuras que se utilizaran
    gpuGreenTriangle = es.toGPUShape(bs.create2ColorTriangle(0.0549, 0.4549, 0.41, 0, 0.8, 0))
    gpuBrownQuad = es.toGPUShape(bs.createColorQuad(0.502, 0.251, 0))


    #Aqui se crean las partes de la copa del pino 
    copa1 = sg.SceneGraphNode("copa1")
    copa1.transform = tr.uniformScale(0.5)
    copa1.childs += [gpuGreenTriangle]
     
    copa2 = sg.SceneGraphNode("copa2")
    copa2.transform = tr.matmul([tr.uniformScale(0.4), tr.translate(0,0.3,0)])
    copa2.childs += [gpuGreenTriangle]
 
    copa3 = sg.SceneGraphNode("copa3")
    copa3.transform = tr.matmul([tr.uniformScale(0.3), tr.translate(0,0.8,0)])
    copa3.childs += [gpuGreenTriangle]

    #Aqui se crea el tronco del arbol 
    tronco = sg.SceneGraphNode("tronco")
    tronco.transform = tr.matmul ([tr.scale(0.1,0.5,0), tr.translate(0, -0.4, 0)])
    tronco.childs += [gpuBrownQuad]

    #Se juntan las partes para crear el arbol 
    arbol = sg.SceneGraphNode("car")
    arbol.childs += [tronco, copa1, copa2, copa3]

    return arbol



def crearBosque(N):

    # Primero escalamos el arbol 
    escalarArbol = sg.SceneGraphNode("escalarArbol")
    escalarArbol.transform = tr.uniformScale(0.5)
    escalarArbol.childs += [crearArbol()]

    bosque = sg.SceneGraphNode("bosque")

    baseName = "arbol"
    for i in range(-N, N+1):
        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode.transform = tr.translate(0.3 * i, 0, 0)
        newNode.childs += [escalarArbol]

        bosque.childs += [newNode] #Se añade la nueva fila de arboles 


    bosqueComp = sg.SceneGraphNode("bosqueComp") #Creamos un bosque con las filas de arboles antes creadas 

    baseName = "fila"    

    for i in range(-5,3): #el objetivo de este for es multiplicar las filas de arboles para crear un bosque 

        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode.transform = tr.translate(0.23*(-1)**i,-0.1*i , 0)
        newNode.childs += [bosque]


        bosqueComp.childs += [newNode]

    return bosqueComp


