import pygame
import numpy as np
from pygame.locals import *



A_x = np.array([
    [1, 0,             0,              0],
    [0, np.cos(600), -np.sin(600), 0],
    [0, np.sin(600),  np.cos(600), 0],
    [0, 0,             0,              1]
])


# Initialize Pygame
width, height = 1000, 1000
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
# theta = 0

# Projection Matrix
fNear, fFar, fFov = 0.1, 1000.0, 90.0
fAspectRatio = height / height 
fFovRad = 1.0 / np.tan(np.radians(fFov / 2))

matProj = np.zeros((4, 4))
fNear, fFar, fFov = 0.1, 10000.0, 120.0
fAspectRatio = height / height
fFovRad = 1.0 / np.tan(np.radians(fFov / 2))
matProj[0][0] = fAspectRatio * fFovRad
matProj[1][1] = fFovRad
matProj[2][2] = fFar / (fFar - fNear)
matProj[3][2] = (-fFar * fNear) / (fFar - fNear)
matProj[2][3] = 1.0
matProj[3][3] = 0.0

fov_y = 60 
aspect = 16/9
near = 0.1
far = 100




def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def Matrix_PointAt(pos, target, up):
    # Calculate new forward direction (from position to target)
    new_forward = normalize(target - pos)

    # Project up onto forward to remove component along forward
    a = new_forward * np.dot(up, new_forward)
    new_up = normalize(up - a)

    # Calculate new right direction as cross product of up and forward
    new_right = np.cross(new_up, new_forward)
    new_right = normalize(new_right)

    # Create 4x4 identity matrix
    matrix = np.identity(4)

    # Set rotation part
    matrix[0, 0:3] = new_right
    matrix[1, 0:3] = new_up
    matrix[2, 0:3] = new_forward
    # matrix[3, 0:3] = pos

    # Set translation part (usually negative position for view matrix)
    matrix[0, 3] = pos[0]
    matrix[1, 3] = pos[1]
    matrix[2, 3] = pos[2]

    return matrix

def look_at(camera_position, camera_target, up_vector):
	vector = camera_position - camera_target
	vector = vector / np.linalg.norm(vector)

	vector2 = np.cross(up_vector, vector)
	vector2 = vector2 / np.linalg.norm(vector2)

	vector3 = np.cross(vector, vector2)
	return np.array([
		[vector2[0], vector3[0], vector[0], 0.0],
		[vector2[1], vector3[1], vector[1], 0.0],
		[vector2[2], vector3[2], vector[2], 0.0],
		[-np.dot(vector2, camera_position), -np.dot(vector3, camera_position), np.dot(vector, camera_position), 1.0]
	])


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

def matrix_quick_inverse(m):
    matrix = np.identity(4)

    # Transpose the rotation part (upper-left 3x3)
    matrix[0][0] = m[0][0]
    matrix[0][1] = m[1][0]
    matrix[0][2] = m[2][0]

    matrix[1][0] = m[0][1]
    matrix[1][1] = m[1][1]
    matrix[1][2] = m[2][1]

    matrix[2][0] = m[0][2]
    matrix[2][1] = m[1][2]
    matrix[2][2] = m[2][2]

    # Inverse translation using dot product
    matrix[3][0] = -(m[3][0] * matrix[0][0] + m[3][1] * matrix[1][0] + m[3][2] * matrix[2][0])
    matrix[3][1] = -(m[3][0] * matrix[0][1] + m[3][1] * matrix[1][1] + m[3][2] * matrix[2][1])
    matrix[3][2] = -(m[3][0] * matrix[0][2] + m[3][1] * matrix[1][2] + m[3][2] * matrix[2][2])
    matrix[3][3] = 1.0

    return matrix


# Load Car Model
vertices, faces = load_obj("./Car.obj")

# Transformations vec will be array of three vectors
def multiply_matrix_vector(mat, vec):
    vec = np.append(vec, 1)  # Convert to 4D
    result = np.dot(mat, vec)
    if result[3] != 0:
        result /= result[3]  # Perspective divide
    return result[:3]

def multiply_matrix_vector_for_triangle(mat, triangle):
    def temp(vec): 
        # vec =  vec+ np.array([0, 0, 30 ])
        vec = np.append(vec, 1)  # Convert to 4D
        result = np.dot(mat, vec)
        if result[3] != 0:
            result /= result[3]  # Perspective divide
        return result[:3]
    newTriangel = [temp(v) for  v in triangle]
    return newTriangel
       

def multiply_matrix_vector2(mat, vec):
    vec = np.append(vec, 1)  # Convert to 4D
    result = np.dot(mat, vec)

    return result[:3]

def x_axis_rotation(theta):
    theta = np.radians(theta)
    return np.array([
        [np.cos(theta), 0, np.sin(theta), 0],
        [0, 1, 0, 0],
        [-np.sin(theta), 0, np.cos(theta), 0],
        [0, 0, 0, 1]  # Correct last row for homogeneous transformation
    ])

def axis_angle_rotation(axis, angle_degrees):
    angle = np.radians(angle_degrees)
    ux, uy, uz = normalize(axis)
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)

    return np.array([
        [cos_theta + ux*ux*(1 - cos_theta),     ux*uy*(1 - cos_theta) - uz*sin_theta, ux*uz*(1 - cos_theta) + uy*sin_theta, 0],
        [uy*ux*(1 - cos_theta) + uz*sin_theta,  cos_theta + uy*uy*(1 - cos_theta),     uy*uz*(1 - cos_theta) - ux*sin_theta, 0],
        [uz*ux*(1 - cos_theta) - uy*sin_theta,  uz*uy*(1 - cos_theta) + ux*sin_theta,  cos_theta + uz*uz*(1 - cos_theta),    0],
        [0, 0, 0, 1]
    ])

def y_axis_rotation(theta):
    theta = np.radians(theta)
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(theta), -np.sin(theta), 0],
        [0, np.sin(theta), np.cos(theta), 0],
        [0, 0, 0, 1]  # Correct last row for homogeneous transformation
    ])
def z_axis_rotation(theta): 
    theta = np.radians(theta)
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(theta), -np.sin(theta), 0],
        [0, np.sin(theta), np.cos(theta), 0],
        [0, 0, 0, 1]  # Correct last row for homogeneous transformation
    ])


def getXY(p):
    scale = 100  # Adjust scale for visibility
    screen_x = int(width / 2 + p[0] * scale)  # Center on screen
    screen_y = int(height / 2 - p[1] * scale)  # Invert Y-axis
    return [screen_x, screen_y, p[2]]
# vertices = [multiply_matrix_vector(A_x, v) for v in vertices]
camaraVector = np.array([0.0, 0.0, 0.0], dtype=float)
# vLookAtMatrix = np.array([4, 0, 1])
vUpVector = np.array([0, 1, 0])
vLookAtMatrix = np.array([0, 0, 1], dtype=float)

theta = 1
count = 1

font = pygame.font.SysFont(None, 24)
def draw_matrix(surface, matrix, pos=(10, 10), color=(0, 255, 0)):
    x, y = pos
    for row in matrix:
        text = font.render(str(np.round(row, 2)), True, color)
        screen.blit(text, (x, y))
        y += 20  # Line spacing
# triangle will be three array with x,y,z values

def planeIntersectPoints(planePoint, normalToPlane, lineStart, lineEnd):
    normalToPlane = normalize(normalToPlane)
    plane_d = -np.dot(normalToPlane, planePoint)
    
    ad = np.dot(lineStart, normalToPlane)
    bd = np.dot(lineEnd, normalToPlane) 
    ratio = (-plane_d - ad) / (bd - ad)
    
    startToEnd = np.subtract(lineEnd, lineStart)
    pointOnPlane = np.multiply(startToEnd, ratio)
    
    return np.add(lineStart, pointOnPlane)

def clipPlane(pointOnPlane, normalToPlane, triangle):
    triangle1 = []
    plane_n = normalize(normalToPlane)
    def dis(point):
        return np.dot(normalToPlane, point) - np.dot(normalToPlane, pointOnPlane)
    insideCounter = 0   
    outsiderCounter = 0    
    insidePoint = []    
    outsidePoints = []    
    d0 = dis(triangle[0])
    d1 = dis(triangle[1])
    d2 = dis(triangle[2])
    if (d0 >= 0):
        insidePoint.append(triangle[0])
        # insidePoint[insideCounter] = triangle[0]
        insideCounter += 1
    else:
        outsidePoints.append(triangle[0] )
        # outsidePoints[outsiderCounter] = triangle[0] 
        outsiderCounter += 1
    if (d1 >= 0):
        #  insidePoint[insideCounter] = triangle[1]
         insidePoint.append(triangle[1])
         insideCounter += 1
    else:
        # outsidePoints[outsiderCounter] = triangle[1] 
        outsidePoints.append(triangle[1] )
        outsiderCounter += 1
    if (d2 >= 0):
        # insidePoint[insideCounter] = triangle[2]
        insidePoint.append(triangle[2])
        insideCounter += 1
    else:   
        # outsidePoints[outsiderCounter] = triangle[2]
        outsidePoints.append(triangle[2])
        outsiderCounter += 1 
    
    if insideCounter == 0:
        return []
    if insideCounter == 3:
        return [triangle]
    if insideCounter == 1 and outsiderCounter == 2 :
        # return one triangles 
        # print(insidePoint)
        triangle[0] = insidePoint[0]
        # y 
        triangle[1] = planeIntersectPoints(pointOnPlane, normalToPlane, insidePoint[0], outsidePoints[0])
        # z
        triangle[2] = planeIntersectPoints(pointOnPlane, normalToPlane, insidePoint[0], outsidePoints[1] )
        return [triangle]
    if insideCounter == 2 and outsiderCounter == 1 :
        
        triangle[0] = insidePoint[0]
        triangle[1] = insidePoint[1]
        triangle[2] = planeIntersectPoints(pointOnPlane, normalToPlane, insidePoint[0], outsidePoints[0])
        triangle1 = []
        # triangle1[0] = insidePoint[0]
        triangle1.append(insidePoint[0])
        # triangle1[1] = triangle[2]
        triangle1.append(triangle[2])
        triangle1.append(planeIntersectPoints(pointOnPlane, normalToPlane, insidePoint[1], outsidePoints[0]))
        
        # triangle1[2] = planeIntersectPoints(pointOnPlane, normalToPlane, insidePoint[1], outsidePoints[0])
        return [triangle, triangle1]




         





    
        
    

    

def render():
    global camaraVector
    global theta
    global vLookAtMatrix
    global vUpVector
    global count
    screen.fill((0, 0, 0)) 
    keys = pygame.key.get_pressed()
    if (keys[K_LSHIFT] or keys[K_RSHIFT]):
        if keys[K_UP]:
            vLookAtMatrix = normalize(multiply_matrix_vector2(y_axis_rotation(theta), vLookAtMatrix))
            vUpVector = normalize(multiply_matrix_vector2(y_axis_rotation(theta), vUpVector))
        elif keys[K_DOWN]:
            vLookAtMatrix = normalize(multiply_matrix_vector2(y_axis_rotation(-theta), vLookAtMatrix))
            vUpVector = normalize(multiply_matrix_vector2(y_axis_rotation(-theta), vUpVector))
        elif keys[K_LEFT]:
            vLookAtMatrix = normalize(multiply_matrix_vector2(x_axis_rotation(theta), vLookAtMatrix))
            vUpVector = normalize(multiply_matrix_vector2(x_axis_rotation(theta), vUpVector))
        elif keys[K_RIGHT]:
          
            vLookAtMatrix = normalize(multiply_matrix_vector2(x_axis_rotation(-theta), vLookAtMatrix))
            
            vUpVector = normalize(multiply_matrix_vector2(x_axis_rotation(-theta), vUpVector))

# Only handle movement if Shift is NOT pressed
    elif not keys[K_LSHIFT] and not keys[K_RSHIFT]:
        if keys[K_w]:
            camaraVector[2] += 0.1  # Move forward
        if keys[K_s]:
            camaraVector[2] -= 0.1  # Move backward
        if keys[K_LEFT]:
            camaraVector[0] -= 0.1  # Move left
        if keys[K_RIGHT]:
            camaraVector[0] += 0.1  # Move right
        if keys[K_DOWN]:
            camaraVector[1] -= 0.1  # Move down
        if keys[K_UP]:
            camaraVector[1] += 0.1  # Move up
    print(vLookAtMatrix)        
    
    matCamera = Matrix_PointAt(camaraVector, camaraVector + vLookAtMatrix, vUpVector)
    
    

    matView = np.linalg.inv(matCamera)
    print(vLookAtMatrix)
    draw_matrix(screen, matCamera , (10, 10), (255, 0, 0))

    transformed_vertices = [multiply_matrix_vector(matView, v) for v in vertices]
    # transformed_vertices = vertices
    # want to to render vLookAtMatrix
    # print(transformed_vertices)
    def createTriangle(f):
        return [transformed_vertices[f[0]], transformed_vertices[f[1]], transformed_vertices[f[2]]]
    # trianglesToRender = [getXY(f) for f in faces]
    trianglesToRender = [createTriangle(f) for f in faces]
    clippedTriangles = []
    for tri in trianglesToRender:
        clipped = clipPlane(np.array([0, 0, 1]), np.array([0, 0, 1]), tri)
        if clipped:
            clippedTriangles.extend(clipped)
    # trianglesToRender = [clipPlane(np.array([0, 0, 1]), np.array([0, 0, 1]), v) for v in trianglesToRender]
    trianglesToRender = clippedTriangles
    
    trianglesToRender = [multiply_matrix_vector_for_triangle(matProj, v) for v in trianglesToRender ]
    np.array([0, 0, 1])
    np.array([0, 0, 1])
    # print(faces[:5], projected_vertices[:5])
    # points = [clipPlane(np.array([0, 0, 1]), np.array([0, 0, 1]), v) for v in projected_vertices]
    # trianglesToRender = [createTriangle(f) for f in faces]
    # points = [getXY(v) for v in projected_vertices]
    # def createTriangle(f):
    #     return [projected_vertices[f[0]], projected_vertices[f[1]], projected_vertices[f[2]]]
    # # trianglesToRender = [getXY(f) for f in faces]
    # trianglesToRender = [createTriangle(f) for f in faces]
    # trianglesToRender = [clipPlane(np.array([0, 0, 1]), np.array([0, 0, 1]), v) for v in trianglesToRender]
    # print(trianglesToRender)
    for f in trianglesToRender:
        if f is None: 
            continue
        # print(f)
        f = [getXY(e) for e in f]
        pygame.draw.line(screen, (255, 255, 255), f[0][:2], f[1][:2])
        pygame.draw.line(screen, (255, 255, 255), f[1][:2], f[2][:2])
        pygame.draw.line(screen, (255, 255, 255), f[2][:2], f[0][:2])

    pygame.display.update()

# Main Loop
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    
    
    render()

pygame.quit()
