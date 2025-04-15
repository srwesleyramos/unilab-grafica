import math

import glfw
import numpy as np
from OpenGL.GL import *


# =================== Inicialização ===================

def init_window(width=600, height=600, title="Laboratório"):
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

    window = glfw.create_window(width, height, title, None, None)

    glfw.make_context_current(window)
    glfw.show_window(window)
    return window


# =================== Shaders ===================

VERTEX_CODE = """
attribute vec2 position;
uniform mat4 transformation;
void main(){
    gl_Position = transformation * vec4(position, 0.0, 1.0);
}
"""

FRAGMENT_CODE = """
uniform vec4 color;
void main(){
    gl_FragColor = color;
}
"""


def create_shader_program():
    program = glCreateProgram()

    # Vertex Shader
    vertex = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex, VERTEX_CODE)
    glCompileShader(vertex)

    if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(vertex).decode())

    # Fragment Shader
    fragment = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment, FRAGMENT_CODE)
    glCompileShader(fragment)

    if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(fragment).decode())

    # Linkando shaders ao programa
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(program))

    glUseProgram(program)
    return program


# =================== Buffers e Geometria ===================

def create_triangle():
    # Define os vértices do triângulo
    vertices = np.zeros(3, [("position", np.float32, 2)])
    vertices['position'] = [(-0.5, 0), (0, 0.5), (0.5, 0)]

    buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
    return vertices, buffer


# =================== Usando o teclado ===================

t_x, t_y, t_z = 0.0, 0.0, 0.0
s_x, s_y, s_z = 1.0, 1.0, 1.0
rotation = 0.0


def key_event(window, key, scancode, action, mods):
    global t_x, t_y
    global s_x, s_y
    global rotation

    if action == 1:
        # Translação

        if key == 265:
            t_y += 0.1

        if key == 264:
            t_y -= 0.1

        if key == 263:
            t_x += 0.1

        if key == 262:
            t_x -= 0.1

        # Escala

        if key == 65:
            s_x += 0.1
            s_y += 0.1

        if key == 68:
            s_x -= 0.1
            s_y -= 0.1

        # Rotação

        if key == 76:
            rotation += 0.1

        if key == 82:
            rotation -= 0.1


# =================== Funções auxiliares ===================

def multiplica_matriz(a, b):
    m_a = a.reshape(4, 4)
    m_b = b.reshape(4, 4)
    m_c = np.dot(m_a, m_b)
    c = m_c.reshape(1, 16)
    return c


# =================== Loop Principal ===================

def main():
    window = init_window()
    program = create_shader_program()
    vertices, buffer = create_triangle()

    # Atributos
    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)
    loc_pos = glGetAttribLocation(program, "position")
    loc_color = glGetUniformLocation(program, "color")
    loc_mat = glGetUniformLocation(program, "transformation")

    glfw.set_key_callback(window, key_event)

    glEnableVertexAttribArray(loc_pos)
    glVertexAttribPointer(loc_pos, 2, GL_FLOAT, False, stride, offset)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Cor do triângulo
        glUniform4f(loc_color, 1.0, 0.0, 0.0, 1.0)

        # Matriz de translação
        mat_translation = np.array([
            1.0, 0.0, 0.0, t_x,
            0.0, 1.0, 0.0, t_y,
            0.0, 0.0, 1.0, t_z,
            0.0, 0.0, 0.0, 1.0
        ], dtype=np.float32)

        # Matriz de escala
        mat_scale = np.array([
            s_x, 0.0, 0.0, 0.0,
            0.0, s_y, 0.0, 0.0,
            0.0, 0.0, s_z, 0.0,
            0.0, 0.0, 0.0, 1.0
        ], dtype=np.float32)

        # Matriz de rotação
        cos_r = math.cos(rotation)
        sin_r = math.sin(rotation)

        mat_rotation = np.array([
            cos_r, -sin_r, 0.0, 0.0,
            sin_r, cos_r, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        ], dtype=np.float32)

        mat_final = multiplica_matriz(multiplica_matriz(mat_translation, mat_rotation), mat_scale)
        glUniformMatrix4fv(loc_mat, 1, GL_TRUE, mat_final)

        # Desenha o triângulo
        glDrawArrays(GL_TRIANGLES, 0, len(vertices))
        glfw.swap_buffers(window)


glfw.terminate()

# =================== Execução ===================

if __name__ == "__main__":
    main()
