import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

#Se importan todas las figuras echas 
import montaña as mn
import auto as at 
import bosque as bq
import casa as cs 
import fondo as fn
import nube as nb 
import nave as nv 

# A class to store the application control
class Controller:
    vf = 0.02 #ponderador de velocidad del fondo
    vm = 2 #ponderador de velocidad de las montañas
    vb = 6 #ponderador de velocidad del bosque
    vc = 12 #ponderador de velocidad de las casas
    dt = 0.1 #el delta tiempo que se utiliza para las flechas izq y der
    auto = [0,0,0] #se "inicia" la variable auto
    light = False #Controlador de la luz del auto 
    turbo = False #Controlador del turbo del auto
    stop = False #Controlador de si el auto esta detenido o no 


# we will use the global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_ESCAPE:
        sys.exit()

    elif key == glfw.KEY_1:
        controller.light = not controller.light
        if controller.light: 
            print("Luces encendidas")
        else: print("Luces apagadas")

    elif key == glfw.KEY_2:
        controller.turbo = not controller.turbo
        if controller.turbo: 
            print("Corre como el viento tiro al blanco")
            if controller.vc > 48:
                print('2')
                controller.vm = controller.vm *4
                controller.vb = controller.vb *4
                controller.vc = controller.vc *4
            else:
                controller.vm = 6
                controller.vb = 12
                controller.vc = 48
        else: 
            print("Quitando el turbo")
            controller.vm = 2
            controller.vb = 6
            controller.vc = 12

    elif key == glfw.KEY_RIGHT:
        print("Acelerando poco a poco (apretar repetidas veces para aumentar mucho la velocidad)" )
        controller.vm += controller.dt
        controller.vb += controller.dt * 4
        controller.vc += controller.dt * 8

    elif key == glfw.KEY_LEFT:
        print("Bajando la velocidad (para retroceder:apretar repetidas veces")
        controller.vm -= controller.dt
        controller.vb -= controller.dt * 4
        controller.vc -= controller.dt * 8

    elif key == glfw.KEY_SPACE:
        controller.stop = not controller.stop
        if controller.stop:
            print("Detener completamente")
            controller.vm = 0
            controller.vb = 0
            controller.vc = 0
        else: 
            print("Volver a la marcha normal")
            controller.vm = 2
            controller.vb = 6
            controller.vc = 12


    else:
        print('Unknown key')




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

    # Setting up the clear screen color
    glClearColor(1, 1, 1, 1)



    # Creating shapes on GPU memory
    # Se crean dos figuras de las que se estan moviendo para poder simular el loop infinito 
    fondo1 = fn.crearfondoDia()
    fondo2 = fn.crearfondoNoche()
    Montanas1 = mn.createMontanas(3)
    Montanas2 = mn.createMontanas(3)
    bosque1 = bq.crearBosque(7)
    bosque2 = bq.crearBosque(7)
    casas1 = cs.crearCyE(2)
    casas2 = cs.crearCyE(2)
    controller.auto = at.createCar(0,0.5412,0.933)
    nave = nv.crearNave()
    nube = nb.crearNubes(2)

    #Se definen las veriables de posicion para las montañas, los bosques y las casas, con los valores necesarios para que 
    #queden una al lado de la otra 
    m = 2.4
    b = 4.5
    c = 5.6
    f = 6

    #Se definen las variables de las posiciones iniciales de cada figura
    pos_m1 = 0
    pos_m2 = m
    pos_c1 = 0
    pos_c2 = c
    pos_b1 = 0
    pos_b2 = b
    pos_f1 = 0
    pos_f2 = f

    #Se declara la variable de velocidad inical como 0
    vel = 0

    #Se crean shifts para cada capa que se mueve (montaña, casa, bosque)
    shift_m = False
    shift_c = False
    shift_b = False
    shift_f = False

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        #Se crea el auto con los contoladores de luz y del tubo 
        controller.auto = at.createCar(0, 0.5412, 0.933, controller.light, controller.turbo) 


        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)


        #Se crea la velocidad utilizando el get_time() para que se muevan las capas
        vel = 10 * glfw.get_time() * 0.003; 
        vel_m = controller.vm * vel
        vel_b = controller.vb * vel
        vel_c = controller.vc * vel
        vel_f = controller.vf * vel



        #Todos los if tienen la misma idea, pero como son variables distintas las variables que se utilizan 
        #deben estar en distintos if. Dentro de estos se crea el movimiento de las capas 

        if(pos_m2 < 0.005 and pos_m2 > -0.005): 
            shift_m = not shift_m

        pos_m1 = vel_m % m
        pos_m2 = (-vel_m + m) % m

        if(shift_m): 
            Montanas1.transform = tr.translate(pos_m2,0,0)
            Montanas2.transform = tr.translate(-pos_m1,0,0)
        else:
            Montanas1.transform = tr.translate(-pos_m1,0,0)
            Montanas2.transform = tr.translate(pos_m2,0,0)




        if(pos_c2 < 0.005 and pos_c2 > -0.005):
            shift_c = not shift_c

        pos_c1 = vel_c % c
        pos_c2 = (-vel_c + c) % c

        if(shift_c):
            casas1.transform = tr.translate(pos_c2,0,0)
            casas2.transform = tr.translate(-pos_c1,0,0)
        else:
            casas1.transform = tr.translate(-pos_c1,0,0)
            casas2.transform = tr.translate(pos_c2,0,0)

      
      

        if(pos_b2 < 0.005 and pos_b2 > -0.005):
            shift_b = not shift_b

        pos_b1 = vel_b % b
        pos_b2 = (-vel_b + b) % b

        if (shift_b):
            bosque1.transform = tr.translate(pos_b2, 0, 0)
            bosque2.transform = tr.translate(-pos_b1, 0, 0)
        else:
            bosque1.transform = tr.translate(-pos_b1, 0, 0)
            bosque2.transform = tr.translate(pos_b2, 0, 0)


        #if (pos_f2 < -0.005 and pos_f2 > -0.005):
        ##    shift_f = not shift_f


        #pos_f1 = vel_f % f
        #pos_f2 = (-vel_f + f) % f

        #if(shift_f):
        #    fondo1.transform = tr.translate(pos_f2,0,0)
        #    fondo2.transform = tr.translate(-pos_f1,0,0)
        #else:
        #    fondo1.transform = tr.translate(-pos_f1,0,0)
        #    fondo2.transform = tr.translate(pos_f2,0,0)

        fondo1.transform = tr.translate(-vel_f,0,0)




        nube.transform = tr.translate(np.sin(2 * vel), 0.1 * np.cos(2*vel),0)
        nave.transform = tr.translate(2*np.sin(vel) -1, 0.2 * np.cos(4*vel),0)




        
 
        
        # Drawing 
        sg.drawSceneGraphNode(fondo1, pipeline, "transform")
        #sg.drawSceneGraphNode(fondo2, pipeline, "transform")
        sg.drawSceneGraphNode(Montanas1, pipeline, "transform")
        sg.drawSceneGraphNode(Montanas2, pipeline, "transform")
        sg.drawSceneGraphNode(nube, pipeline, "transform")
        #La nave se crea antes que el bosque para que el marcianito se esconda detras de los arboles
        sg.drawSceneGraphNode(nave, pipeline, "transform") 
        sg.drawSceneGraphNode(bosque2, pipeline, "transform")
        sg.drawSceneGraphNode(bosque1, pipeline, "transform")
        sg.drawSceneGraphNode(casas1, pipeline, "transform")
        sg.drawSceneGraphNode(casas2, pipeline, "transform")
        sg.drawSceneGraphNode(controller.auto, pipeline, "transform")



        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()