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


def crearCasa(pos):

    gpuBeigeQuad = es.toGPUShape(bs.createColorQuad(1,0.8667,0.749))
    gpuRedTriangle = es.toGPUShape(bs.createColorTriangle(1,0.1961,0.4314))
    gpuSBQuad = es.toGPUShape(bs.createColorQuad(0.6588,0.9686,1))
    gpuOrangeQuad = es.toGPUShape(bs.createColorQuad(1,0.5176,0.3412))
    gpuBlackCirc = es.toGPUShape(bs.createCircle([0,0,0]))
    gpuBrownQuad = es.toGPUShape(bs.createColorQuad(0.6039,0.2039,0))
    gpuPQuad = es.toGPUShape(bs.createColorQuad(0.8392,0.749,1))

    #Se crea la base de la casa 
    base = sg.SceneGraphNode("base")
    base.transform = tr.uniformScale(0.4)
    base.childs += [gpuBeigeQuad] 
    
    # Se crea el techo de la casa
    techo = sg.SceneGraphNode("techo")
    techo.transform = tr.matmul([tr.translate(0,0.3,0) ,tr.scale(0.6,0.2,1)])
    techo.childs += [gpuRedTriangle]

    #Se crean las ventanas con sus respectivos marcos 
    ventD = sg.SceneGraphNode("ventD")
    ventD.transform = tr.matmul([tr.translate(0.1,0.1,0) ,tr.uniformScale(0.1)])
    ventD.childs += [gpuSBQuad]

    marcoVD = sg.SceneGraphNode("marcoVD")
    marcoVD.transform = tr.matmul([tr.translate(0.1,0.1,0) ,tr.uniformScale(0.12)])
    marcoVD.childs += [gpuBrownQuad]

    ventI = sg.SceneGraphNode("ventI")
    ventI.transform = tr.matmul([tr.translate(-0.1,0.1,0) ,tr.uniformScale(0.1)])
    ventI.childs += [gpuSBQuad]

    marcoVI = sg.SceneGraphNode("marcoVI")
    marcoVI.transform = tr.matmul([tr.translate(-0.1,0.1,0) ,tr.uniformScale(0.12)])
    marcoVI.childs += [gpuBrownQuad]

    #Se crea la puerta 
    puerta = sg.SceneGraphNode("puerta")
    puerta.transform = tr.matmul([tr.scale(0.1,0.2,1), tr.translate(0,-0.5,0)])
    puerta.childs += [gpuOrangeQuad]

    #Se crea el marco de la puerta 
    marcoP = sg.SceneGraphNode("marcoP")
    marcoP.transform = tr.matmul([tr.scale(0.12,0.21,1), tr.translate(0,-0.45,0)])
    marcoP.childs += [gpuBrownQuad]

    #Se crea la manilla de la puerta 
    mani = sg.SceneGraphNode("mani")
    mani.transform = tr.matmul ([tr.translate(-0.03,-0.1,0),tr.uniformScale(0.009)])
    mani.childs += [gpuBlackCirc]

    #Se crea un camino de entrada a la casa 
    camino = sg.SceneGraphNode("camino")
    camino.transform = tr.matmul([tr.translate(0,-0.23,0), tr.scale(0.12,0.06,1)])
    camino.childs += [gpuPQuad]
    
    #Se crea la casa con todas su componentes 
    casa = sg.SceneGraphNode("casa")
    casa.childs += [base, techo, marcoVD, ventD, marcoVI, ventI, marcoP, puerta, mani, camino]

    #Trasladamos la casa segun la posicion que se le indique 
    traslatedCasa = sg.SceneGraphNode("traslatedCar")
    traslatedCasa.transform = tr.translate(pos, 0,0)
    traslatedCasa.childs += [casa]

    return traslatedCasa


def crearEntorno():

    gpuGreenTriangle = es.toGPUShape(bs.create2ColorTriangle(0.3059,0.7804,0, 0.6706,1,0.7137))
    gpuGrayQuad = es.toGPUShape(bs.createColorQuad(0.5,0.5,0.5))
    gpuGreenQuad = es.toGPUShape(bs.createColorQuad(0.3529, 1, 0.5659))

    #Se crea un pequeño pastito 
    #pastito = sg.SceneGraphNode("pastito")
    #pastito.transform = tr.uniformScale(0.08)
    #pastito.childs += [gpuGreenTriangle]  
    
    #pastitos = sg.SceneGraphNode("pastitos")
    #baseName="pastitos"

    #for i in range(-24,25): #se crea este for para hacer una fila de pastitos  
        # A new node is only locating a scaledCar in the scene depending on index i
        #newNode = sg.SceneGraphNode(baseName + str(i))
        #newNode.transform = tr.translate(0.04 * i, 0, 0)
        #newNode.childs += [pastito]

        # Now this car is added to the 'cars' scene graph
        #pastitos.childs += [newNode]


    #pastitos2 = sg.SceneGraphNode("pastitos2")
    #baseName="pastitos2"

    #for i in range(-15,12): #el objetivo de este for es multiplicar las filas de pastitos 

        #newNode = sg.SceneGraphNode(baseName + str(i))
        #newNode.transform = tr.translate(0.01*(-1)**i,-0.02*i , 0)
        #newNode.childs += [pastitos]


        #pastitos2.childs += [newNode]

        #Toda la parte comentada era mi idea de hacer un pasto mas "realista" con los materiales que hemos visto hasta el 
        #momento pero era mucho trabajo para el computador por lo que la imagen estaba cortada cuando se reproducía 


    #Esta es la opcion B del pasto
    pasto = sg.SceneGraphNode("pasto")
    pasto.transform = tr.matmul([tr.translate(0,-0.035,0) , tr.scale(2,0.45,1)])
    pasto.childs += [gpuGreenQuad]

    #Se crea el muro de la derecha
    murod = sg.SceneGraphNode("murod")
    murod.transform = tr.matmul ([tr.translate(1,0.04,0),tr.scale(0.08,0.6,1)])
    murod.childs += [gpuGrayQuad]

    #Se crea el muro de la izquierda
    muroi = sg.SceneGraphNode("muroi")
    muroi.transform = tr.matmul ([tr.translate(-1,0.04,0),tr.scale(0.08,0.6,1)])
    muroi.childs += [gpuGrayQuad]

    #Se crea el muro de la divisor
    murodiv = sg.SceneGraphNode("murodiv")
    murodiv.transform = tr.matmul ([tr.translate(0,0.04,0),tr.scale(0.08,0.6,1)])
    murodiv.childs += [gpuGrayQuad]

    #Se crea el muro trasero
    murot = sg.SceneGraphNode("murot")
    murot.transform = tr.matmul ([tr.translate(0,0.09,0),tr.scale(2,0.5,1)])
    murot.childs += [gpuGrayQuad]


    entorno = sg.SceneGraphNode("entorno")
    entorno.childs += [murot, pasto, murod, muroi, murodiv]


    return entorno


def crearCyE (N): #Se crea la casa y el entorno 

    #Esta funcion creara un par de casas en un mismo entorno 
    todo = sg.SceneGraphNode("todo")
    todo.transform = tr.uniformScale(0.7)
    todo.childs = [crearEntorno(), crearCasa(0.5), crearCasa(-0.5)]

    casas = sg.SceneGraphNode("casas")

    baseName = "casas"

    for i in range(-N,N): #Aqui creamos casas dobles 2n veces   

        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode.transform = tr.translate(1.4 * i, -0.5, 0) 
        newNode.childs += [todo]

        casas.childs += [newNode]

    return casas

