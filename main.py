import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import time
# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
theta = np.radians(5)
# Set up perspectiv

A_y = np.array([
    [np.cos(theta),  0, np.sin(theta), 0],
    [0,              1, 0,             0],
    [-np.sin(theta), 0, np.cos(theta), 0],
    [0,              0, 0,             1]  # Correct last row for homogeneous transformation
])

A_z = np.array([
    [np.cos(theta), -np.sin(theta), 0, 0],
    [np.sin(theta),  np.cos(theta), 0, 0],
    [0,              0,             1, 0],
    [0,              0,             0, 1]
])

A_x = np.array([
    [1,  0,            0,             0],
    [0,  np.cos(theta), -np.sin(theta), 0],
    [0,  np.sin(theta),  np.cos(theta), 0],
    [0,  0,            0,             1]
])

def multiply_matrix_vector(m, i):
    x = i[0] * m[0][0] + i[1] * m[1][0] + i[2] * m[2][0] + m[3][0]
    y = i[0] * m[0][1] + i[1] * m[1][1] + i[2] * m[2][1] + m[3][1]
    z = i[0] * m[0][2] + i[1] * m[1][2] + i[2] * m[2][2] + m[3][2]
    w = i[0] * m[0][3] + i[1] * m[1][3] + i[2] * m[2][3] + m[3][3]

    if w != 0.0:
        x /= w
        y /= w
        z /= w

    return np.array([x, y, z])


def transform_point(matrix, point):
    """
    Multiplies a 4x4 matrix with a 4D point (homogeneous coordinates).
    Applies perspective division.
    """
    point_h = np.array([point[0], point[1], point[2], 1.0])  # Convert to homogeneous coordinates
    transformed = matrix @ point_h  # Matrix-vector multiplication
    w = transformed[3]  # Extract w component
    if w != 0:  
        transformed /= w  # Perspective division
    print(w)
    return transformed[:3]


def projection_matrix(fov, aspect_ratio, near, far):
    fov_rad = 1.0 / np.tan(np.radians(fov) / 2.0)

    mat_proj = np.zeros((4, 4))
    mat_proj[0][0] = aspect_ratio * fov_rad
    mat_proj[1][1] = fov_rad
    mat_proj[2][2] = far / (far - near)
    mat_proj[3][2] = (-far * near) / (far - near)
    mat_proj[2][3] = 1.0
    mat_proj[3][3] = 0.0

    return mat_proj

def perspective_projection(fov, aspect, near, far):
    """
    Creates a perspective projection matrix.
    
    :param fov: Field of View in degrees
    :param aspect: Aspect ratio (width / height)
    :param near: Near clipping plane
    :param far: Far clipping plane
    :return: 4x4 projection matrix
    """
    f = 1.0 / np.tan(np.radians(fov) / 2)
    depth = far - near

    return np.array([
        [f / aspect, 0,  0,                              0],
        [0,          f,  0,                              0],
        [0, 0, -(far + near) / depth, -2 * (far * near) / depth],
        [0,          0, 1,                              0]
    ], dtype=np.float32)

def perspective_projection2(fov, aspect, near, far):
    """
    Creates a perspective projection matrix.
    
    :param fov: Field of View in degrees
    :param aspect: Aspect ratio (width / height)
    :param near: Near clipping plane
    :param far: Far clipping plane
    :return: 4x4 projection matrix
    """
    f = 1.0 / np.tan(np.radians(fov) / 2)
    depth = far - near

    return np.array([
        [1, 0,  0,                              0],
        [0,          1,  0,                              0],
        [0, 0, 0, 0],
        [0,          0, 0,                              0]
    ], dtype=np.float32)


fov = 90  # Field of view in degrees
aspect = 8/6  # Screen aspect ratio
near = 0.1  # Near clipping plane
far = 1000.0  # Far clipping plane

matrix_44 = perspective_projection(fov, aspect, near, far)

f_near = 0.1
f_far = 1000.0
f_fov = 90.0
f_aspect_ratio = 1080 / 1920  # Example screen dimensions

mat_proj = projection_matrix(f_fov, f_aspect_ratio, f_near, f_far)



vertices = np.array([
    # SOUTH
    [[-1.0, -1.0, -1.0],    [-1.0,  1.0, -1.0],    [ 1.0,  1.0, -1.0]],
    [[-1.0, -1.0, -1.0],    [ 1.0,  1.0, -1.0],    [ 1.0, -1.0, -1.0]],

    # EAST
    [[ 1.0, -1.0, -1.0],    [ 1.0,  1.0, -1.0],    [ 1.0,  1.0,  1.0]],
    [[ 1.0, -1.0, -1.0],    [ 1.0,  1.0,  1.0],    [ 1.0, -1.0,  1.0]],

    # NORTH
    [[ 1.0, -1.0,  1.0],    [ 1.0,  1.0,  1.0],    [-1.0,  1.0,  1.0]],
    [[ 1.0, -1.0,  1.0],    [-1.0,  1.0,  1.0],    [-1.0, -1.0,  1.0]],

    # WEST
    [[-1.0, -1.0,  1.0],    [-1.0,  1.0,  1.0],    [-1.0,  1.0, -1.0]],
    [[-1.0, -1.0,  1.0],    [-1.0,  1.0, -1.0],    [-1.0, -1.0, -1.0]],

    # TOP
    [[-1.0,  1.0, -1.0],    [-1.0,  1.0,  1.0],    [ 1.0,  1.0,  1.0]],
    [[-1.0,  1.0, -1.0],    [ 1.0,  1.0,  1.0],    [ 1.0,  1.0, -1.0]],

    # BOTTOM
    [[ 1.0, -1.0,  1.0],    [-1.0, -1.0,  1.0],    [-1.0, -1.0, -1.0]],
    [[ 1.0, -1.0,  1.0],    [-1.0, -1.0, -1.0],    [ 1.0, -1.0, -1.0]],
], dtype=np.float32)

# vertices = np.array([
#     # SOUTH
#     [[0.0, 0.0, 0.0],    [0.0, 1.0, 0.0],    [1.0, 1.0, 0.0]],
#     [[0.0, 0.0, 0.0],    [1.0, 1.0, 0.0],    [1.0, 0.0, 0.0]],

#     # EAST
#     [[1.0, 0.0, 0.0],    [1.0, 1.0, 0.0],    [1.0, 1.0, 1.0]],
#     [[1.0, 0.0, 0.0],    [1.0, 1.0, 1.0],    [1.0, 0.0, 1.0]],

#     # NORTH
#     [[1.0, 0.0, 1.0],    [1.0, 1.0, 1.0],    [0.0, 1.0, 1.0]],
#     [[1.0, 0.0, 1.0],    [0.0, 1.0, 1.0],    [0.0, 0.0, 1.0]],

#     # WEST
#     [[0.0, 0.0, 1.0],    [0.0, 1.0, 1.0],   [ 0.0, 1.0, 0.0]],
#     [[0.0, 0.0, 1.0],    [0.0, 1.0, 0.0],    [0.0, 0.0, 0.0]],

#     # TOP
#     [[0.0, 1.0, 0.0],    [0.0, 1.0, 1.0],    [1.0, 1.0, 1.0]],
#     [[0.0, 1.0, 0.0],    [1.0, 1.0, 1.0],    [1.0, 1.0, 0.0]],

#     # BOTTOM
#     [[1.0, 0.0, 1.0],    [0.0, 0.0, 1.0],    [0.0, 0.0, 0.0]],
#     [[1.0, 0.0, 1.0],    [0.0, 0.0, 0.0],    [1.0, 0.0, 0.0]],
# ], dtype=np.float32)




def drawTriangle2D(first, second, third):
    glBegin(GL_LINE_LOOP)  # Draws the edges of a triangle
    glVertex2fv(first)
    glVertex2fv(second)
    glVertex2fv(third)
    glEnd()



edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]
A = np.array([
    [np.cos(theta), -np.sin(theta), 0],
    [np.sin(theta),  np.cos(theta), 0],
     [0,  0, 1],
])


matProj = np.zeros((4, 4))
fNear, fFar, fFov = 0.1, 1000.0, 120.0
fAspectRatio = 800 / 600
fFovRad = 1.0 / np.tan(np.radians(fFov / 2))
matProj[0][0] = fAspectRatio * fFovRad
matProj[1][1] = fFovRad
matProj[2][2] = fFar / (fFar - fNear)
matProj[3][2] = (-fFar * fNear) / (fFar - fNear)
matProj[2][3] = 1.0
matProj[3][3] = 0.0



def draw_cube(vertices):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex2fv(vertices[vertex])
    glEnd()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    transformed_vertices = []
    for index, triangle in enumerate(vertices):
    #    triangle[0] = multiply_matrix_vector(A_x, triangle[0])
    #    triangle[1] = multiply_matrix_vector(A_x, triangle[1])
    #    triangle[2] = multiply_matrix_vector(A_x, triangle[2])

       triangle[0] = multiply_matrix_vector(A_x, triangle[0])
       triangle[1] = multiply_matrix_vector(A_x, triangle[1])
       triangle[2] = multiply_matrix_vector(A_x, triangle[2])

    #    triangle[0] = multiply_matrix_vector(A_z, triangle[0])
    #    triangle[1] = multiply_matrix_vector(A_z, triangle[1])
    #    triangle[2] = multiply_matrix_vector(A_z, triangle[2])
       

       
      
       transformedA = list(triangle[0])
       transformedB = list(triangle[1])
       transformedC = list(triangle[2])
       transformedA[2] = triangle[0][2] + 3.00
       transformedB[2] = triangle[1][2] + 3.00
       transformedC[2] = triangle[2][2] + 3.00
       
       a = multiply_matrix_vector(matProj, transformedA)
       b = multiply_matrix_vector(matProj, transformedB)
       c = multiply_matrix_vector(matProj, transformedC)
       
       screen.fill((0, 0, 0))
       
       
       drawTriangle2D(
            [a[0], a[1]],
            [b[0], b[1]],
            [c[0], c[1]]
       )

    time.sleep(0.3)
    pygame.display.flip()
    pygame.time.wait(30)


