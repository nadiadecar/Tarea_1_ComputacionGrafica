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


def createCar(r,g,b,foc=False,turbo=False):

    if not foc: #El proposito de este if es cambiar las luces delanteras del auto, de manera que si foc != False, los focos estan prendidos (amarillos) 
        rf = 0.8
        gf = 0.8
        bf = 0.8
    else: #Aqui se aplica el color amarillo para el caso de que foc no sea False 
        rf = 0.9686
        gf = 0.9412
        bf = 0

    #Se crean las figuras que se utilizaran para la creacion del auto 
    gpuBlackCirc = es.toGPUShape(bs.createCircle([0,0,0]))
    gpuWhiteCirc = es.toGPUShape(bs.createCircle([0.8,0.8,0.8]))
    gpuBlueQuad = es.toGPUShape(bs.createColorQuad(r,g,b)) #Se dejan los colores como variables para que Don Pedro pueda elegir el color de auto que mas le gusta 
    gpuFocQuad = es.toGPUShape(bs.createColorQuad(rf,gf,bf))
    gpuRedQuad = es.toGPUShape(bs.createColorQuad(1,0,0))
    gpuSBQuad = es.toGPUShape(bs.createColorQuad(0.5922,0.9569, 1))

    #Se crea la parte interna de la rueda de color blanco 
    little_wheel = sg.SceneGraphNode("little_wheel")
    little_wheel.transform = tr.uniformScale(0.08)
    little_wheel.childs += [gpuWhiteCirc] 
    
    # Se crea la parte negra de la rueda (la más externa)
    big_wheel = sg.SceneGraphNode("big_wheel")
    big_wheel.transform = tr.uniformScale(0.2)
    big_wheel.childs += [gpuBlackCirc]

    #Se crea la rueda completa compuesta de las dos partes anteriores
    wheel = sg.SceneGraphNode("wheel")
    wheel.childs += [big_wheel, little_wheel]


    wheelRotation = sg.SceneGraphNode("wheelRotation")
    wheelRotation.childs += [wheel]

    # Se instalan las dos ruedas en el auto 
    frontWheel = sg.SceneGraphNode("frontWheel")
    frontWheel.transform = tr.translate(0.5,-0.3,0)
    frontWheel.childs += [wheelRotation]

    backWheel = sg.SceneGraphNode("backWheel")
    backWheel.transform = tr.translate(-0.5,-0.3,0)
    backWheel.childs += [wheelRotation]
    
    # Se crear el chasis del auto 
    chasis = sg.SceneGraphNode("chasis")
    chasis.transform = tr.scale(1.8,0.5,1)
    chasis.childs += [gpuBlueQuad]

    #Se crea el techo del auto 
    techo = sg.SceneGraphNode("techo")
    techo.transform = tr.matmul([ tr.translate(0,0.45,0), tr.scale(1,0.5,1)])
    techo.childs += [gpuBlueQuad]

    #Se crea el foco trasero
    foco_tras = sg.SceneGraphNode("foco_tras")
    foco_tras.transform = tr.matmul ([tr.translate(-0.86,0.21,0),tr.scale(0.08,0.08,1)])
    foco_tras.childs += [gpuRedQuad]

    #Se crea el foco delantero 
    foco_del = sg.SceneGraphNode("foco_del")
    foco_del.transform = tr.matmul ([tr.translate(0.86,0.21,0),tr.scale(0.08,0.08,1)])
    foco_del.childs += [gpuFocQuad]

    #Se crean las ventanas del auto 
    vent_der = sg.SceneGraphNode("vent_der")
    vent_der.transform = tr.matmul ([tr.translate(0.23,0.45,0),tr.scale(0.38,0.37,1)])
    vent_der.childs += [gpuSBQuad]
 
    vent_izq = sg.SceneGraphNode("vent_izq")
    vent_izq.transform = tr.matmul ([tr.translate(-0.23,0.45,0),tr.scale(0.38,0.37,1)])
    vent_izq.childs += [gpuSBQuad]

    #Se creal auto compuesto de todas las partes anteriormente creadas
    car = sg.SceneGraphNode("car")
    car.childs += [chasis, techo, frontWheel, backWheel, foco_tras, foco_del, vent_der, vent_izq]

    #Se traslada y escala el auto
    scaledCar = sg.SceneGraphNode("scaledCar")
    scaledCar.transform = tr.matmul([tr.translate(0,-0.66,0) , tr.uniformScale(0.15)])
    scaledCar.childs += [car]


    #Se crean las figras que se utilizaran para el turbo 
    gpuGrayOv = es.toGPUShape(bs.createSemiCircle([0.7,0.7,0.7]))
    gpuBlackC = es.toGPUShape(bs.createCircle([0.2,0.2,0.2]))
    gpuRYC = es.toGPUShape(bs.create2ColorCircle([1,0,0], [1,0.9961,0.4392]))

    #La base de la turbina 
    base = sg.SceneGraphNode("base")
    base.transform = tr.matmul([tr.rotationZ(-np.pi/2) , tr.scale(0.04,0.17,1)])
    base.childs += [gpuGrayOv]

    baseTr = sg.SceneGraphNode("baseTr")
    baseTr.transform = tr.translate(-0.07,-0.515,0)
    baseTr.childs += [base]

    #Se crea la parte trasera de la turbina en conjunto con el "fuego" que lo impulsa  
    fin = sg.SceneGraphNode("fin")
    fin.transform = tr.matmul([tr.translate(-0.07,-0.515,0) , tr.scale(0.02,0.04,1)])
    fin.childs += [gpuBlackC]

    fuego = sg.SceneGraphNode("fuego")
    fuego.transform = tr.matmul ([tr.translate(-0.07,-0.515,0) , tr.scale(0.01,0.03,1)])
    fuego.childs = [gpuRYC]

    #Se crea la turbina
    turboT = sg.SceneGraphNode("turbo")
    turboT.childs += [baseTr, fin, fuego]

    #Creamos una figura que va a ir cambiando los childs dependiendo de si el turbo esta activo o no 
    autoFinal = sg.SceneGraphNode("autoFinal")
    autoFinal.childs += [] 


    if turbo==False: #en el caso de que el turbo este desactivado se crea solo el auto escalado y trasladado
        autoFinal.childs = [scaledCar]
    elif turbo==True: #cuando la turbina esta activa el auto se compone de la turbina y el auto escalado 
        autoFinal.childs = [turboT, scaledCar]
    else: autoFinal.childs =[]



    return autoFinal