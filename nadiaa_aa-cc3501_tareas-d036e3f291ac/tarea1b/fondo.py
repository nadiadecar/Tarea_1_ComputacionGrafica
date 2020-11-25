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

    if key == glfw.KEY_SPACE:
    	print("FALLA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    else:
        print('Unknown key')


def crearfondoDia():

	gpuGrayQuad = es.toGPUShape(bs.createColorQuad(0.2, 0.2, 0.2))
	gpuSkyQuad = es.toGPUShape(bs.create2ColorQuad(1,1,1, 0.7373, 0.9961, 1))
	gpuGreenQuad = es.toGPUShape(bs.createColorQuad(0.6706,1,0.7137))
	gpuYellowCirc = es.toGPUShape(bs.create2ColorCircle([1,0.9961,0.4392],[1,1,1]))

	#Creamos el cielo con un degradado de blanco a celeste 
	cielo = sg.SceneGraphNode("cielo")
	cielo.transform = tr.matmul([tr.translate(0,0.5,0),tr.scale(6,1.75,1)])
	cielo.childs += [gpuSkyQuad]

	#Creamos el camino para el auto 
	asfalto = sg.SceneGraphNode("asfalto")
	asfalto.transform = tr.matmul([tr.translate(0,-0.75,0),tr.scale(6,0.5,1)])
	asfalto.childs += [gpuGrayQuad]

	#Se crea el pasto que se vera entre los arboles 
	pasto = sg.SceneGraphNode("pasto")
	pasto.transform = tr.matmul([tr.translate(0,-0.2,0) , tr.scale(6,0.7,1)])
	pasto.childs += [gpuGreenQuad]

	#Creamos un sol en la esquina de la pantalla
	sol = sg.SceneGraphNode("sol")
	sol.transform = tr.matmul([tr.translate(1,1,0), tr.uniformScale(0.3)])
	sol.childs += [gpuYellowCirc]

	fondo = sg.SceneGraphNode("fondo")
	fondo.childs += [cielo, asfalto, pasto, sol]



	return fondo



def crearfondoNoche():

	gpuGrayQuad = es.toGPUShape(bs.createColorQuad(0.1, 0.1, 0.1))
	gpuSkyQuad = es.toGPUShape(bs.create2ColorQuad(1,1,1, 0.1451, 0.1569, 0.3137))
	gpuGreenQuad = es.toGPUShape(bs.createColorQuad(0.3059,0.651,0.3294))
	gpuGrayCirc = es.toGPUShape(bs.create2ColorCircle([0.6941,0.7216,0.7218],[0.8784,0.8902,0.8902]))

	#Creamos el cielo con un degradado de blanco a azul cielo 
	cielo = sg.SceneGraphNode("cielo")
	cielo.transform = tr.matmul([tr.translate(0,0.5,0),tr.scale(6,1.75,1)])
	cielo.childs += [gpuSkyQuad]

	#Creamos el camino para el auto 
	asfalto = sg.SceneGraphNode("asfalto")
	asfalto.transform = tr.matmul([tr.translate(0,-0.75,0),tr.scale(6,0.5,1)])
	asfalto.childs += [gpuGrayQuad]

	#Se crea el pasto que se vera entre los arboles 
	pasto = sg.SceneGraphNode("pasto")
	pasto.transform = tr.matmul([tr.translate(0,-0.2,0) , tr.scale(6,0.7,1)])
	pasto.childs += [gpuGreenQuad]

	#Creamos una luna en la esquina de la pantalla
	luna = sg.SceneGraphNode("luna")
	luna.transform = tr.matmul([tr.translate(1,1,0), tr.uniformScale(0.3)])
	luna.childs += [gpuGrayCirc]

	fondo = sg.SceneGraphNode("fondo")
	fondo.childs += [cielo, asfalto, pasto, luna]

	return fondo

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Paseo de don pedro", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen colors
    glClearColor(1, 1, 1, 1)



    # Creating shapes on GPU memory
    # Se crean dos figuras de las que se estan moviendo para poder simular el loop infinito 
    fondo1 = crearfondoDia()
    fondo2 = crearfondoNoche()


    f = 3

    pos_f1 = 0
    pos_f2 = f

    #Se declara la variable de velocidad inical como 0
    vel = 0


    shift_f = False

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        #Se crea el auto con los contoladores de luz y del tubo 



        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)


        #Se crea la velocidad utilizando el get_time() para que se muevan las capas
        vel = 10 * glfw.get_time() * 0.003; 

        vel_f = 20 * vel
        print (pos_f2)




        if (pos_f2 < 0.005 and pos_f2 > -0.005): 
        	shift_f = not shift_f



        pos_f1 = vel_f % f
        pos_f2 = (-vel_f + f) % f

        if(shift_f): 
            fondo1.transform = tr.translate(pos_f2,0,0)
            fondo2.transform = tr.translate(-pos_f1,0,0)
        else:
            fondo1.transform = tr.translate(-pos_f1,0,0)
            fondo2.transform = tr.translate(pos_f2,0,0)





        sg.drawSceneGraphNode(fondo1, pipeline, "transform")
        sg.drawSceneGraphNode(fondo2, pipeline, "transform")




        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()


