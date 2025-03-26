import pygame
import numpy as np
from pygame.locals import *

# Initialize Pygame
width, height = 1000, 1000
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
theta = 0

# Projection Matrix
fNear, fFar, fFov = 0.1, 1000.0, 45.0
fAspectRatio = width / height
fFovRad = 1.0 / np.tan(np.radians(fFov / 2))

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

# Function to Load an OBJ File
def load_obj(filename):
    vertices = []
    faces = []

    with open(filename, "r") as file:
        for line in file:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "v":  # Vertex position
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif parts[0] == "f":  # Face (triangles only)
                face = [int(parts[i].split('/')[0]) - 1 for i in range(1, 4)]
                faces.append(face)

    return np.array(vertices, dtype=np.float32), np.array(faces, dtype=np.int32)

# Load Car Model
vertices, faces = load_obj("./Car.obj")

# Transformations
def multiply_matrix_vector(mat, vec):
    vec = np.append(vec, 1)  # Convert to 4D
    result = np.dot(mat, vec)
    if result[3] != 0:
        result /= result[3]  # Perspective divide
    return result[:3]


def getXY(p):
    scale = 100  # Adjust scale for visibility
    screen_x = int(width / 2 + p[0] * scale)  # Center on screen
    screen_y = int(height / 2 - p[1] * scale)  # Invert Y-axis
    return [screen_x, screen_y]

def render():
    screen.fill((0, 0, 0)) 

    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta), 0, 0],
        [np.sin(theta),  np.cos(theta), 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1],
    ])
    A_z = np.array([
        [np.cos(theta),  0, np.sin(theta), 0],
        [0,              1, 0,             0],
        [-np.sin(theta), 0, np.cos(theta), 0],
        [0,              0, 0,             1]  # Correct last row for homogeneous transformation
    ])

    A_x = np.array([
    [1, 0,             0,              0],
    [0, np.cos(9.773000000000017), -np.sin(9.773000000000017), 0],
    [0, np.sin(9.773000000000017),  np.cos(9.773000000000017), 0],
    [0, 0,             0,              1]
    ])

    # print(theta)

    transformed_vertices = [multiply_matrix_vector(A_x, v ) for v in vertices]
    transformed_vertices = [multiply_matrix_vector(A_z, v ) for v in transformed_vertices]
    
    projected_vertices = [multiply_matrix_vector(matProj, v + np.array([0, 0, 10])) for v in transformed_vertices]
    points = [getXY(v) for v in projected_vertices]

    for f in faces:
        pygame.draw.line(screen, (255, 255, 255), points[f[0]], points[f[1]])
        pygame.draw.line(screen, (255, 255, 255), points[f[1]], points[f[2]])
        pygame.draw.line(screen, (255, 255, 255), points[f[2]], points[f[0]])

    pygame.display.update()

# Main Loop
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    theta += dt
    render()

pygame.quit()
