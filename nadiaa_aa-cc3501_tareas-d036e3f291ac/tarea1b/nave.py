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



def crearNave():

	gpuBCirc = es.toGPUShape(bs.createCircle([0,0.4627,0.4118]))
	gpuBlackCirc = es.toGPUShape(bs.createCircle([0,0,0]))
	gpuSBCirc = es.toGPUShape(bs.createSemiCircle([0,0,0]))
	gpuSGreenCirc = es.toGPUShape(bs.createSemiCircle([0.4392,1,0.4078]))
	gpuGreenCirc = es.toGPUShape(bs.createCircle([0.4392,1,0.4078]))
	gpuBlackQuad = es.toGPUShape(bs.createColorQuad(0,0,0))
	gpuGreenQuad = es.toGPUShape(bs.createColorQuad(0.4392,1,0.4078))

	#Se crea la parte mas grande de la nave (asi como el chasis de auto)
	base = sg.SceneGraphNode("base")
	base.transform = tr.scale(0.5,0.08,0)
	base.childs += [gpuBCirc]

	#Creamos el "vidrio" de la nave, que es la parte donde podemos ver al marcianito, se crea negro para que sea mas facil ver la nave 
	#y al marciano debido a que con los colores del fondo la nave se pierde 
	vidrio = sg.SceneGraphNode("vidrio")
	vidrio.transform = tr.matmul([tr.translate(0,0.02,0),tr.scale(0.2,0.35,0)])
	vidrio.childs += [gpuSBCirc]

	#Se crean las patas de la nave, compuestas por una bolita negra y un rectangulo del mismo color 
	pataIzq = sg.SceneGraphNode("pataIzq")
	pataIzq.transform = tr.matmul([tr.rotationZ(np.pi/5) ,tr.scale(0.02,0.25,0)])
	pataIzq.childs += [gpuBlackQuad]

	pataDer = sg.SceneGraphNode("pataDer")
	pataDer.transform = tr.matmul([tr.rotationZ(-(np.pi/5)) ,tr.scale(0.02,0.25,0)])
	pataDer.childs += [gpuBlackQuad]

	pataItras = sg.SceneGraphNode("pataItras")
	pataItras.transform = tr.translate(0.3,-0.1,0)
	pataItras.childs += [pataIzq]

	pataDtras = sg.SceneGraphNode("pataDtras")
	pataDtras.transform = tr.translate(-0.3,-0.1,0)
	pataDtras.childs += [pataDer]

	finPataI = sg.SceneGraphNode("finPataI")
	finPataI.transform = tr.matmul([tr.translate(0.375,-0.2,0) ,tr.uniformScale(0.025)])
	finPataI.childs += [gpuBlackCirc]

	finPataD = sg.SceneGraphNode("finPataD")
	finPataD.transform = tr.matmul([tr.translate(-0.375,-0.2,0) ,tr.uniformScale(0.025)])
	finPataD.childs += [gpuBlackCirc]

	pataD = sg.SceneGraphNode("pataD")
	pataD.childs += [pataDtras, finPataD]

	pataI = sg.SceneGraphNode("pataI")
	pataI.childs += [pataItras, finPataI]

	#Creamos al marcianito 

	#Se crea primero el cuerpo
	cuerpoTripulacion = sg.SceneGraphNode("cuerpoTripulacion")
	cuerpoTripulacion.transform = tr.matmul([tr.translate(0,0.02,0), tr.scale(0.03,0.06,0)]) 
	cuerpoTripulacion.childs += [gpuSGreenCirc]

	#Creamos la cabeza
	cabezaTripulacion = sg.SceneGraphNode("cabezaTripulacion")
	cabezaTripulacion.transform = tr.matmul([tr.translate(0,0.12,0) , tr.uniformScale(0.04)])
	cabezaTripulacion.childs += [gpuGreenCirc]

	#Aqui creamos las antenas completas del marcianito, con una idea muy parecida a las patas de la nave
	antenaD = sg.SceneGraphNode("antenaD")
	antenaD.transform = tr.matmul([tr.translate(0.017,0.165,0) ,tr.scale(0.01,0.025,0)])
	antenaD.childs += [gpuGreenQuad]

	antenaI = sg.SceneGraphNode("antenaI")
	antenaI.transform = tr.matmul([tr.translate(-0.017,0.165,0),tr.scale(0.01,0.025,0)])
	antenaI.childs += [gpuGreenQuad]

	finAnD = sg.SceneGraphNode("finAnD")
	finAnD.transform = tr.matmul([tr.translate(0.017,0.19,0) , tr.uniformScale(0.015)])
	finAnD.childs = [gpuGreenCirc]

	finAnI = sg.SceneGraphNode("finAnI")
	finAnI.transform = tr.matmul([tr.translate(-0.017,0.19,0) , tr.uniformScale(0.015)])
	finAnI.childs = [gpuGreenCirc]		

	#Se  crea la nave en conjunto con la tripulacion
	nave = sg.SceneGraphNode("nave")
	nave.transform = tr.matmul([tr.translate(0,0.7,0) , tr.uniformScale(0.1)])
	nave.childs += [pataI, pataD, base, vidrio, cuerpoTripulacion, cabezaTripulacion, antenaD, antenaI, finAnD, finAnI]

	#Se crea esto para luego poder trasladar la nave en la parte final 
	navef = sg.SceneGraphNode("navef")
	navef.childs += [nave]


	return navef


