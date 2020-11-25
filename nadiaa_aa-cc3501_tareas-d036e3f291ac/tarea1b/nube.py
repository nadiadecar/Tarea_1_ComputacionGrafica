import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

import fondo as fn 

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


def crearNube():
	gpuWhiteCirc = es.toGPUShape(bs.createCircle([0.95,0.95,0.95]))

	#Se crea la base de la nube 
	circulito = sg.SceneGraphNode("circulito")
	circulito.transform = tr.uniformScale(0.02)
	circulito.childs += [gpuWhiteCirc]

	base = sg.SceneGraphNode("base")

	baseName = "base"

	for i in range(-5,4): #Se utiliza esto para crear la parte inicial de la nube 
		newNode = sg.SceneGraphNode(baseName + str(i))
		newNode.transform = tr.translate(0.015*i,0.011*(-1)**i,0)
		newNode.childs += [circulito]

		base.childs += [newNode]

	nube = sg.SceneGraphNode("nube")

	baseName1 = "nube"

	for i in range(0,2): #Se crea la parte de abajo de la nube 
		newNode = sg.SceneGraphNode(baseName1 + str(i))
		newNode.transform = tr.matmul([tr.translate(-0.03*(i-1),-0.04*i,0), tr.rotationZ(np.pi*i)])
		newNode.childs += [base]

		nube.childs += [newNode]

	nubeAlta = sg.SceneGraphNode("nubeAlta")
	nubeAlta.transform = tr.translate(0,0.8,0)
	nubeAlta.childs += [nube]



	return nubeAlta


def crearNubes(N):

	#esta funcion se utiliza para crear 2n nubes en la pantalla
	nubes = sg.SceneGraphNode("nubes")

	baseName = "nubes"

	for i in range(-N,N):
		newNode = sg.SceneGraphNode(baseName+str(i))
		newNode.transform = tr.translate(0.99*i,0.05*(-1)**i,0)
		newNode.childs += [crearNube()]

		nubes.childs +=[newNode]

	return nubes


