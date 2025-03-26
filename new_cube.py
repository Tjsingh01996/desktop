
import pygame
import numpy as np
from pygame.locals import *
width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
theta = 0
matProj = np.zeros((4, 4))
fNear, fFar, fFov = 0.1, 10000.0, 120.0
fAspectRatio = 800 / 600
fFovRad = 1.0 / np.tan(np.radians(fFov / 2))
matProj[0][0] = fAspectRatio * fFovRad
matProj[1][1] = fFovRad
matProj[2][2] = fFar / (fFar - fNear)
matProj[3][2] = (-fFar * fNear) / (fFar - fNear)
matProj[2][3] = 1.0
matProj[3][3] = 0.0

A = np.array([
    [np.cos(theta), -np.sin(theta), 0],
    [np.sin(theta),  np.cos(theta), 0],
     [0,  0, 1],
])

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

def multiply_matrix_vector(mat, vec):
    vec = np.append(vec, 1)  # Convert to 4D
    result = np.dot(mat, vec)
    if result[3] != 0:
        result /= result[3]  # Perspective divide
    return result[:3]


def getXY(p):
   scale = 30  # Sc
   screen_x = int(width / 2 + p[0] * scale)  # Center the cube on screen
   screen_y = int(height / 2 - p[1] * scale)  # Invert Y-axis for proper orientation
   return [screen_x, screen_y]


def AddINZ(p):
    p[2] += 3 
    return p 



def render():
    screen.fill((0, 0, 0))
    A = np.array([
        [np.cos(theta), -np.sin(theta), 0, 0],
        [np.sin(theta),  np.cos(theta), 0, 0],
        [0,  0, 1,0],
         [0,  0, 0,1],
    ])
    A_y = np.array([
        [np.cos(theta),  0, np.sin(theta), 0],
        [0,              1, 0,             0],
        [-np.sin(theta), 0, np.cos(theta), 0],
        [0,              0, 0,             1]  # Correct last row for homogeneous transformation
    ])
    projected_vertices = []
    for tries in vertices:
        
        # updated = [AddINZ(vertex) for vertex in tries]
        # print(updated)
        # print(updated)
        rotatedX = [multiply_matrix_vector(A_y, vertex) for vertex in tries]
        rotatedXy = [multiply_matrix_vector(A, vertex) for vertex in rotatedX]
       
        rotatedXy[0][2] = 8
        rotatedXy[1][2] = 8
        rotatedXy[2][2] = 8
        projected = [multiply_matrix_vector(matProj, vertex) for vertex in rotatedXy]
       
        points = [getXY(vertex) for vertex in projected]
        pygame.draw.line(screen, (255, 255, 255), points[0], points[1])
        pygame.draw.line(screen, (255, 255, 255), points[1], points[2])
        pygame.draw.line(screen, (255, 255, 255), points[2], points[0])
    pygame.display.update()    
    


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

while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    

    theta +=  dt
    render()
pygame.quit()