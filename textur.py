from operator import ge
import pygame
import numpy as np
from pygame.locals import *
from dataclasses import dataclass
width = 1000 
height = 1000
screen = pygame.display.set_mode((width, height))
texture = pygame.image.load('./input.png').convert()
aspectRatio = height / width 

pygame.init()


@dataclass
class Vec3D:
    x: float
    y: float
    z: float
    w: float 

    def to_array(self):
        return np.array([self.x, self.y, self.z])
    def to_array_with_w(self):
        return np.array([self.x, self.y, self.z, self.w])

@dataclass
class UV:
    u: float
    v: float

@dataclass
class Vertex:
    pos: Vec3D
    uv: UV
    # add method to Vertex
    def toArray(self):
        return np.array([self.pos.x, self.pos.y, self.pos.z, self.pos.w ])

@dataclass
class Triangle:
    v1: Vertex
    v2: Vertex
    v3: Vertex


cube_vertices = [
    # SOUTH
    Triangle(
        Vertex(Vec3D(0, 0, 0, 1), UV(1, 1)),
        Vertex(Vec3D(0, 1, 0, 1), UV(1, 0)),
        Vertex(Vec3D(1, 1, 0, 1), UV(0, 0))
    ),
    Triangle(
        Vertex(Vec3D(0, 0, 0, 1), UV(1, 1)),
        Vertex(Vec3D(1, 1, 0, 1), UV(0, 0)),
        Vertex(Vec3D(1, 0, 0, 1), UV(0, 1))
    ),

    # EAST
    Triangle(
        Vertex(Vec3D(1, 0, 0, 1), UV(1, 1)),
        Vertex(Vec3D(1, 1, 0, 1), UV(0, 1)),
        Vertex(Vec3D(1, 1, 1, 1), UV(0, 0))
    ),
    Triangle(
        Vertex(Vec3D(1, 0, 0, 1), UV(1, 1)),
        Vertex(Vec3D(1, 1, 1, 1), UV(0, 0)),
        Vertex(Vec3D(1, 0, 1, 1), UV(1, 0))
    ),

    # NORTH
    Triangle(
        Vertex(Vec3D(1, 0, 1, 1), UV(1, 1)),
        Vertex(Vec3D(1, 1, 1, 1), UV(0, 1)),
        Vertex(Vec3D(0, 1, 1, 1), UV(0, 0))
    ),
    Triangle(
        Vertex(Vec3D(1, 0, 1, 1), UV(1, 1)),
        Vertex(Vec3D(0, 1, 1, 1), UV(0, 0)),
        Vertex(Vec3D(0, 0, 1, 1), UV(1, 0))
    ),

    # WEST
    Triangle(
        Vertex(Vec3D(0, 0, 1, 1), UV(1, 1)),
        Vertex(Vec3D(0, 1, 1, 1), UV(0, 1)),
        Vertex(Vec3D(0, 1, 0, 1), UV(0, 0))
    ),
    Triangle(
        Vertex(Vec3D(0, 0, 1, 1), UV(1, 1)),
        Vertex(Vec3D(0, 1, 0, 1), UV(0, 0)),
        Vertex(Vec3D(0, 0, 0, 1), UV(1, 0))
    ),

    # TOP
    Triangle(
        Vertex(Vec3D(0, 1, 0, 1), UV(1, 1)),
        Vertex(Vec3D(0, 1, 1, 1), UV(1, 0)),
        Vertex(Vec3D(1, 1, 1, 1), UV(0, 0))
    ),
    Triangle(
        Vertex(Vec3D(0, 1, 0, 1), UV(1, 1)),
        Vertex(Vec3D(1, 1, 1, 1), UV(0, 0)),
        Vertex(Vec3D(1, 1, 0, 1), UV(0, 1))
    ),

    # BOTTOM
    Triangle(
        Vertex(Vec3D(1, 0, 1, 1), UV(1, 1)),
        Vertex(Vec3D(0, 0, 1, 1), UV(1, 0)),
        Vertex(Vec3D(0, 0, 0, 1), UV(0, 0))
    ),
    Triangle(
        Vertex(Vec3D(1, 0, 1, 1), UV(1, 1)),
        Vertex(Vec3D(0, 0, 0, 1), UV(0, 0)),
        Vertex(Vec3D(1, 0, 0, 1), UV(0, 1))
    ),
]

# need to read about perspective projection matrix
def perspective_projection_matrix(fov_deg, aspect_ratio, near, far):
    fov_rad = np.radians(fov_deg)
    f = 1.0 / np.tan(fov_rad / 2.0)

    matrix = np.array([ 
        [f / aspect_ratio, 0,  0,                           0],
        [0,                f,  0,                           0],
        [0,                0,  (far) / (far - near),        1],
        [0,                0, -(near * far) / (far - near), 0]
    ], dtype=np.float32)    

    return matrix


def getVector3dFromNumpyArray(array: np.ndarray) -> Vec3D:
    if array.shape[0] == 3:
        return Vec3D(array[0], array[1], array[2], 0.0)  # w = 0 for direction vector
    elif array.shape[0] == 4:
        return Vec3D(array[0], array[1], array[2], array[3])  # w is included
    else:
        raise ValueError("Array must be of shape (3,) or (4,)")



def normalOfTwoVector(a: Vec3D, b: Vec3D) -> Vec3D:
    normal = np.cross(a.to_array(), b.to_array())
    norm = np.linalg.norm(normal)
    if norm != 0:
        normal = normal / norm
    return Vec3D(normal[0], normal[1], normal[2], 0.0)  # w = 0 for direction vector

def multiplyTwoVectors(a: Vec3D, b: Vec3D) -> Vec3D:
    return np.dot(a.to_array_with_w(), b.to_array_with_w())  # w = 0 for direction vector

def subtractVertex(a: Vec3D, b: Vec3D) -> Vec3D :
    v1 = np.array(a.to_array())
    v2 = np.array(b.to_array())
    result = v1 - v2
    return Vec3D(result[0], result[1], result[2], 0.0)
    


def x_axis_rotation(theta):
    theta = np.radians(theta)
    return np.array([
        [np.cos(theta), 0, np.sin(theta), 0],
        [0, 1, 0, 0],
        [-np.sin(theta), 0, np.cos(theta), 0],
        [0, 0, 0, 1]  # Correct last row for homogeneous transformation
    ])

def y_axis_rotation(theta):
    theta = np.radians(theta)
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(theta), -np.sin(theta), 0],
        [0, np.sin(theta), np.cos(theta), 0],
        [0, 0, 0, 1]  # Correct last row for homogeneous transformation
    ])

def multiply_matrix_vector(m, v:Vertex):
    # Convert Vertex to Vec3D for matrix multiplication
    vec = v.pos.to_array()
    vec = np.append(vec, 1)  # Append 1 for homogeneous coordinates
    result = np.dot(m, vec)
    pos = Vec3D(result[0] , result[1], result[2], result[3])
    # Convert back to Vec3D
    return Vertex(pos=pos, uv=v.uv) 

def divideByW(vec: Vec3D):
        if hasattr(vec, "w") and vec.w != 0:
            vec.x /= vec.w
            vec.y /= vec.w
            vec.z /= vec.w
        return vec
   
def divideTriangleByW(triangle: Triangle) -> Triangle:
    v1 = triangle.v1
    v1.pos = divideByW(v1.pos)

    v2 = triangle.v2
    v2.pos = divideByW(v2.pos)

    v3 = triangle.v3
    v3.pos = divideByW(v3.pos)

    return Triangle(v1=v1, v2=v2, v3=v3)



def multiplyTriangleWithMatrix(triangle: Triangle, matrix):
   return Triangle(
        v1=multiply_matrix_vector(matrix, triangle.v1),
        v2=multiply_matrix_vector(matrix, triangle.v2),
        v3=multiply_matrix_vector(matrix, triangle.v3)
    ) 


def updateVector(vertex:Vertex):
        scale = 300  # Adjust this value to change the size of the triangle
        pos = Vec3D(int(width / 2 + vertex.pos.x * scale), int(height / 2 - vertex.pos.y * scale), int(vertex.pos.z * scale), 1)
        return Vertex(pos=pos, uv=vertex.uv)


def updateTriangle(triangle: Triangle) -> Triangle:
    # Example transform (scaling positions)
    return Triangle(
        v1=updateVector(triangle.v1),
        v2=updateVector(triangle.v2),
        v3=updateVector(triangle.v3)
    )


def drawTriangle(triangle: Triangle, color):
    # Adjust scale for visibility
    p1 = triangle.v1.pos
    p2 = triangle.v2.pos
    p3 = triangle.v3.pos  # Invert Y-axis
   
    pygame.draw.line(screen, (255, 255, 255), [p1.x, p1.y], [p2.x, p2.y])
    pygame.draw.line(screen, (255, 255, 255), [p2.x, p2.y], [p3.x, p3.y])
    pygame.draw.line(screen, (255, 255, 255), [p3.x, p3.y], [p1.x, p1.y])

    # pygame.draw.polygon(screen, color, [p1, p2, p3])
def normalize(vector: Vec3D):
    norm = np.linalg.norm(vector.to_array())
    if norm == 0:
        return Vec3D(vector[0], vector[1], vector[2], vector[3])
    vector = vector.to_array_with_w() / norm
    return Vec3D(vector[0], vector[1], vector[2], vector[3])


def getCamera(up: Vec3D, lookAt: Vec3D, position: Vec3D):

    # Create a camera matrix based on the up vector, lookAt vector, and position
    z_axis = subtractVertex(lookAt, position)
    z_axis = normalize(z_axis)  # Normalize the z-axis vector

    x_axis = normalOfTwoVector(up, z_axis)  # Calculate the x-axis vector as the cross product of up and z-axis
    x_axis = normalize(x_axis)  # Normalize the x-axis vector
    # Calculate the y-axis vector as the cross product of z-axis and x-axis

    y_axis = normalOfTwoVector(z_axis, x_axis)  # Calculate the y-axis vector as the cross product of z-axis and x-axis
    y_axis = normalize(y_axis)  # Normalize the y-axis vector
    # Create the camera matrix

    # Compute the translation (camera position affects negatively in view matrix)
    tx = -multiplyTwoVectors(x_axis, position)
    ty = -multiplyTwoVectors(y_axis, position)
    tz = -multiplyTwoVectors(z_axis, position)
    camera_matrix = np.array([
        [x_axis.x, y_axis.x, z_axis.x, tx],
        [x_axis.y, y_axis.y, z_axis.y, ty],
        [x_axis.z, y_axis.z, z_axis.z, tz],
        [0, 0, 0, 1]  # Correct last row for homogeneous transformation
    ], dtype=np.float32)

    return camera_matrix

def runWindow():
    clock = pygame.time.Clock()
    running = True 
    
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        run(dt)
    pygame.quit()

# cube_vertices = [updateTriangle(t) for t in cube_vertices]
worldViewMatrix = perspective_projection_matrix(90, aspectRatio, 1, 500)
i = 1

cameraPosition = Vec3D(0, 0, -6, 1)
lookAtVector = Vec3D(0, 0, 1, 1)
upVector = Vec3D(0, 1, 0, 1)

def updateCameraPosition(pressedKey: pygame.key.ScancodeWrapper, cameraPosition: Vec3D, lookAtVector: Vec3D, upVector: Vec3D):
    movementSpeed = 0.1  # Adjust the speed of camera movement
    #  increase the speed of camera movement
    if pressedKey[pygame.K_LSHIFT] or pressedKey[pygame.K_RSHIFT]:
        movementSpeed *= 3

    if pressedKey[pygame.K_UP]:  # Move Upword
        cameraPosition.y += movementSpeed
        lookAtVector.y += movementSpeed
    if pressedKey[pygame.K_DOWN]:  # Move Downword
        cameraPosition.y -= movementSpeed
        lookAtVector.y -= movementSpeed
    if pressedKey[pygame.K_LEFT]:  # Move Left
        cameraPosition.x -= movementSpeed
        lookAtVector.x -= movementSpeed
    if pressedKey[pygame.K_RIGHT]:  # Move Right
        cameraPosition.x += movementSpeed
        lookAtVector.x += movementSpeed
    if pressedKey[pygame.K_w] :  # Move backward with shift + Up key
        cameraPosition.z -= movementSpeed
        lookAtVector.z -= movementSpeed
    if pressedKey[pygame.K_s]:  # Move forward with shift + Down key
        cameraPosition.z += movementSpeed
        lookAtVector.z += movementSpeed    

    return cameraPosition, lookAtVector, upVector

translation_matrix = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],  # push forward by 3 units
    [0, 0, 0, 1]
], dtype=np.float32)

# Get the camera matrix
def run(dt):
    global i
    global cameraPosition, lookAtVector, upVector
    keys = pygame.key.get_pressed()
    cameraPosition, lookAtVector, upVector = updateCameraPosition(keys, cameraPosition, lookAtVector, upVector)

    cameraMatrix = getCamera(upVector, lookAtVector, cameraPosition)
    inverseCameraMatrix = np.linalg.inv(cameraMatrix)
    screen.fill((0, 0, 0))  # Clear screen with black

    rotationMatrix_y = y_axis_rotation(i)
    triangles = cube_vertices
    triangles = [multiplyTriangleWithMatrix(t, rotationMatrix_y) for t in triangles]
    
    triangles = [divideTriangleByW(multiplyTriangleWithMatrix(t, worldViewMatrix @ inverseCameraMatrix )) for t in triangles]

    
    triangles = [updateTriangle(t) for t in triangles]
    

    
    i += 1
    # print(triangles)
    for t in triangles:
        line = subtractVertex(t.v1.pos, t.v2.pos)
        line2 = subtractVertex(t.v3.pos, t.v1.pos)
        normalVector = normalOfTwoVector(line, line2)
        # drawTriangle(t, (255, 255, 255))
        if(multiplyTwoVectors(getVector3dFromNumpyArray(cameraMatrix[2]),normalVector) > 0):
            drawTriangle(t, (255, 255, 255))
            draw_texture(t, texture)  # Load and draw texture
    
        
    pygame.display.flip()  # Update the display
    
    return

# Draw the texture on the triangle
def draw_texture(triangle:Triangle, texture):
    x1 =  triangle.v1.pos.x
    y1 =  triangle.v1.pos.y
    z1 =  triangle.v1.pos.z
    u1 = triangle.v1.uv.u
    v1 = triangle.v1.uv.v

    x2 =  triangle.v2.pos.x
    y2 =  triangle.v2.pos.y
    z2 =  triangle.v2.pos.z
    u2 = triangle.v2.uv.u
    v2 = triangle.v2.uv.v

    x3 =  triangle.v3.pos.x
    y3 =  triangle.v3.pos.y
    z3 =  triangle.v3.pos.z
    u3 = triangle.v3.uv.u
    v3 = triangle.v3.uv.v

    if y2 < y1:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        u1, u2 = u2, u1
        v1, v2 = v2, v1
    if y3 < y1:
        x1, x3 = x3, x1
        y1, y3 = y3, y1
        u1, u3 = u3, u1
        v1, v3 = v3, v1
    if y3 < y2:
        x2, x3 = x3, x2
        y2, y3 = y3, y2
        u2, u3 = u3, u2
        v2, v3 = v3, v2
    if y1:
        #  Calculate steps from y1 to y2 
        dx1Step = (x2 - x1) / (y2 - y1) if y2 != y1 else 0
        du1Step = (u2 - u1) / (y2 - y1) if y2 != y1 else 0
        dv1Step = (v2 - v1) / (y2 - y1) if y2 != y1 else 0

        dx2Step = (x3 - x1) / (y3 - y1) if y3 != y1 else 0
        du2Step = (u3 - u1) / (y3 - y1) if y3 != y1 else 0
        dv2Step = (v3 - v1) / (y3 - y1) if y3 != y1 else 0



        for y in range(int(y1), int(y2) + 1):
            # calculate x and u,v for the first edge
            dx1 = int(x1 + dx1Step * (y - y1))
            du1 = u1 + du1Step * (y - y1)
            dv1 = v1 + dv1Step * (y - y1)
            # calculate x and u,v for the second edge
            dx2 = int(x1 + dx2Step * (y - y1))
            du2 = u1 + du2Step * (y - y1)
            dv2 = v1 + dv2Step * (y - y1)

            if dx1 > dx2:
                dx1, dx2 = dx2, dx1
                du1, du2 = du2, du1
                dv1, dv2 = dv2, dv1

            # Draw horizontal line from dx1 to dx2
            # step = (dx2 - dx1) // max(1, dx2 - dx1)
            # step u with respective to dx1 and dx2 for u and v
            texture_u_step = (du2 - du1) / (dx2 - dx1) if dx2 != dx1 else 0
            texture_v_step = (dv2 - dv1) / (dx2 - dx1) if dx2 != dx1 else 0 
            for x in range(dx1, dx2 + 1):

                u = du1 + texture_u_step * (x - dx1)
                v = dv1 + texture_v_step * (x - dx1)

                hu = int(u * texture.get_width())
                hv = int(v * texture.get_height())
                # hu = int(du1 + texture_u_step * (x - dx1))
                # hv = int(dv1 + texture_v_step * (x - dx1))
                if 0 <= x < width and 0 <= y < height:
                    color = texture.get_at((hu % texture.get_width(), hv % texture.get_height()))
                    screen.set_at((x, y), color)

    if y3 > y2:
        # Calculate steps from y2 to y3
        dx1Step = (x3 - x2) / (y3 - y2) if y3 != y2 else 0
        du1Step = (u3 - u2) / (y3 - y2) if y3 != y2 else 0
        dv1Step = (v3 - v2) / (y3 - y2) if y3 != y2 else 0

        dx2Step = (x3 - x1) / (y3 - y1) if y3 != y1 else 0
        du2Step = (u3 - u1) / (y3 - y1) if y3 != y1 else 0
        dv2Step = (v3 - v1) / (y3 - y1) if y3 != y1 else 0

        for y in range(int(y2), int(y3) + 1):
            # calculate x and u,v for the first edge
            dx1 = int(x2 + dx1Step * (y - y2))
            du1 = u2 + du1Step * (y - y2)
            dv1 = v2 + dv1Step * (y - y2)
            # calculate x and u,v for the second edge
            dx2 = int(x1 + dx2Step * (y - y1))
            du2 = u1 + du2Step * (y - y1)
            dv2 = v1 + dv2Step * (y - y1)

            if dx1 > dx2:
                dx1, dx2 = dx2, dx1
                du1, du2 = du2, du1
                dv1, dv2 = dv2, dv1

            # Draw horizontal line from dx1 to dx2
            texture_u_step = (du2 - du1) / (dx2 - dx1) if dx2 != dx1 else 0
            texture_v_step = (dv2 - dv1) / (dx2 - dx1) if dx2 != dx1 else 0 
            for x in range(dx1, dx2 + 1):
                u = du1 + texture_u_step * (x - dx1)
                v = dv1 + texture_v_step * (x - dx1)
                hu = int(u * texture.get_width())
                hv = int(v * texture.get_height())
                if 0 <= x < width and 0 <= y < height:
                    color = texture.get_at((hu % texture.get_width(), hv % texture.get_height()))
                    screen.set_at((x, y), color)     

runWindow()
