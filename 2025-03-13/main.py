import glfw
from OpenGL.GL import *
import numpy as np

glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(600, 600, "Linhas", None, None)
glfw.make_context_current(window)

VERTEX_CODE = """
        attribute vec2 position;
        void main(){
            gl_Position = vec4(position,0.0,1.0);
        }
        """
FRAGMENT_CODE = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
        """

program = glCreateProgram()
vertex = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)

glShaderSource(vertex, VERTEX_CODE)
glShaderSource(fragment, FRAGMENT_CODE)
glCompileShader(vertex)

if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")

glCompileShader(fragment)

if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")

glAttachShader(program, vertex)
glAttachShader(program, fragment)
glLinkProgram(program)

if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')

glUseProgram(program)

def bresenham(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    slope = dy / dx

    if slope > 1:
        dx, dy = dy, dx
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    p = 2 * dy - dx
    x, y = x1, y1

    points = [(x, y)]

    for i in range(dx):
        if p < 0:
            p += 2 * dy
        else:
            p += 2 * (dy - dx)
            y += 1 if y2 > y1 else -1
        x += 1 if x2 > x1 else -1

        points.append((x, y))

    return points

po = bresenham(1, 3, 5, 11)

def pontosdaReta(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    b = y1-m*x1
    points = []

    for x in range(x2):
        y = m*x+b
        points.append((x, y))

    points.append((x2, y2))
    return points

pontos = pontosdaReta(1, 3, 5, 11)
normalized_input = (pontos - np.amin(pontos)) / (np.amax(pontos) - np.amin(pontos))
g = normalized_input.tolist()
print(g)

vertices = np.zeros(len(pontos), [("position", np.float32, 2)])
vertices['position'] =  g #[(-1,0),(0,1),(0,0)]
buffer = glGenBuffers(1)

glBindBuffer(GL_ARRAY_BUFFER, buffer)

buffer = glGenBuffers(1)

glBindBuffer(GL_ARRAY_BUFFER, buffer)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, buffer)

stride = vertices.strides[0]
offset = ctypes.c_void_p(0)

loc = glGetAttribLocation(program, "position")
loc_color = glGetUniformLocation(program, "color")

R = 1.0
G = 0.0
B = 0.0

glEnableVertexAttribArray(loc)
glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

glfw.show_window(window)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)  
    glUniform4f(loc_color, R, G, B, 1.0)
    glPointSize(10.0)
    glDrawArrays(GL_POINTS, 0, len(vertices))
    glfw.swap_buffers(window)

glfw.terminate()
