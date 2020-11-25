import glfw # Usada para interactuar con un usuario (mouse, teclado, etc)
from OpenGL.GL import * # importa las funciones de OpenGL
import OpenGL.GL.shaders # importa el set de shaders de OpenGL.
import numpy as np
import sys # handling de eventos, entradas del sistema, o cerrar el programa.


# A class to store the application control
class Controller:
    fillPolygon = True
    shader_to_use = 0

# We will use the global controller as communication with the callback function
controller = Controller() # Here we declare this as a global variable.

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller # Declares that we are going to use the global object controller inside this function.

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon
        print("Toggle GL_FILL/GL_LINE")

    elif key == glfw.KEY_ENTER:
        # controller.useShader2 = not controller.useShader2
        # Usamos % 3 para que nunca supere el 3. Será 0, 1 ó 2. Cuando llegue a 3 o algo superior, se volverá a mover a 
        # entre 0, 1 ó 2. Compruébelo!
        controller.shader_to_use = (controller.shader_to_use + 1) % 3
        print("Toggle shader program")

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


# A simple class container to reference a shape on GPU memory
class GPUShape:
    def __init__(self):
        self.vao = 0
        self.vbo = 0
        self.ebo = 0
        self.texture = 0
        self.size = 0


def drawShape(shaderProgram, shape):

    # Binding the proper buffers
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

    # Setting up the location of the attributes position and color from the VBO
    # A vertex attribute has 3 integers for the position (each is 4 bytes),
    # and 3 numbers to represent the color (each is 4 bytes),
    # Henceforth, we have 3*4 + 3*4 = 24 bytes
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)
    
    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # Render the active element buffer with the active shader program
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)

def creadpolig(n):

    # Here the new shape will be stored
    gpuShape = GPUShape()

    phi = (2*np.pi)/n
    r = 1

    vertex=[0,0,0,1,1,1,r,0,0,0.2471,0.5333,0.5608]

    indices=[]

    for i in range(1,n+1):
    	punto=[r*np.cos(phi*i),r*np.sin(phi*i),0,0.2471,0.5333,0.5608]
    	vertex += punto
    	indices += [0, i, i+1]

    vertexData = np.array(vertex, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)
    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * 4, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * 4, indices, GL_STATIC_DRAW) 

    return gpuShape





if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Teletubis", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)


    # Defining shaders for our pipeline
    vertex_shader = """
    #version 130
    in vec3 position;
    in vec3 color;

    out vec3 fragColor;

    void main()
    {
        fragColor = color;
        gl_Position = vec4(position, 1.0f);
    }
    """

    fragment_shader = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor, 1.0f);
    }
    """

    fragment_shader2 = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;
    void main()
    {
        float meanColor = (fragColor.r + fragColor.g + fragColor.b) / 3;
        outColor = vec4(meanColor, meanColor, meanColor,  1.0f);
    }
    """
    

    fragment_shader_night = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor.r * 0.2, fragColor.g * 0.2, (fragColor.b + 0.2) * 0.5, 1.0f);
    }
    """


# #### Declaración de los pipelines de rendering.
# Se indica cuál se usa cuando se ejecuta glUseProgram(__ciertoShaderProgram__) y drawshape(__ciertoShaderProgram__, gpuAlgo) 

# Assembling the shader program (pipeline) with both shaders
shaderProgram = OpenGL.GL.shaders.compileProgram(
    OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
    OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

shaderProgram2 = OpenGL.GL.shaders.compileProgram(
    OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
    OpenGL.GL.shaders.compileShader(fragment_shader2, GL_FRAGMENT_SHADER))

shaderProgram_night = OpenGL.GL.shaders.compileProgram(
    OpenGL.GL.shaders.compileShader(
vertex_shader, GL_VERTEX_SHADER),
    OpenGL.GL.shaders.compileShader(fragment_shader_night, GL_FRAGMENT_SHADER))


# Setting up the clear screen color
glClearColor(0.15, 0.15, 0.15, 1.0) 


# #### Creación de las figuras en la memoria GPU
# No es necesario que estén juntas, pero sí se recomienda. <br>

# Creating shapes on GPU memory
ricardo = int(input('Numero de lados: '))
gpuPolygon = creadpolig(ricardo)


while not glfw.window_should_close(window):
    # Using GLFW to check for input events
    glfw.poll_events()

    # Filling or not the shapes depending on the controller state
    if (controller.fillPolygon):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Clearing the screen in both, color and depth
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shaderProgram)
    # Telling OpenGL to draw our shapes using the previous shader program.
    drawShape(shaderProgram, gpuPolygon)        
        
    # Once the render is done, buffers are swapped, showing only the complete scene.
    glfw.swap_buffers(window)

glfw.terminate()


#Se deberia crear una función que divida los 360 grados o
#los 2 pi en la cantidad de lados que se le entregan a la 
#función con lo que se crean las posiciones para las esquinas 
#y a partir de eso se crea una matriz con las posiciones 
#hay que utilizar coordenadas cilindricas x=pcos(phi)
#y=psin(phi)
#phi=2pi/n
#La parte de dphi se utilizara para crear las uniones de los
#puntos 
