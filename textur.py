import pygame
import numpy as np
from pygame.locals import *
import colorsys
from dataclasses import dataclass
width = 1000 
height = 1000
screen = pygame.display.set_mode((width, height))
texture = pygame.image.load('./input.png').convert()
   





@dataclass
class Vec3D:
    x: float
    y: float
    z: float

    def to_array(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])

@dataclass
class UV:
    u: float
    v: float

@dataclass
class Vertex:
    pos: Vec3D
    uv: UV

@dataclass
class Triangle:
    v1: Vertex
    v2: Vertex
    v3: Vertex


cube_vertices = [
    Triangle(
    Vertex(Vec3D(0, 0, 0), UV(1, 1)),
    Vertex(Vec3D(1, 0, 0), UV(1, 0)),
    Vertex(Vec3D(0, 1, 0), UV(0, 1))
),
Triangle(
    Vertex(Vec3D(1, 0, 0), UV(1, 0)),
    Vertex(Vec3D(1, 1, 0), UV(0, 0)),
    Vertex(Vec3D(0, 1, 0), UV(0, 1))
),
]

def perspective_projection_matrix(fov_deg, aspect_ratio, near, far):
    fov_rad = np.radians(fov_deg)
    f = 1.0 / np.tan(fov_rad / 2.0)

    matrix = np.array([
        [f / aspect_ratio, 0,  0,                           0],
        [0,                f,  0,                           0],
        [0,                0,  (near + far) / (near - far), (2 * near * far) / (near - far)],
        [0,                0, -1,                           0]
    ], dtype=np.float32)

    return matrix


# def multiply_matrix_vector(m, v):
   
def updateVector(vertex:Vertex):
        scale = 300  # Adjust this value to change the size of the triangle
        pos = Vec3D(int(width / 2 + vertex.pos.x * scale), int(height / 2 - vertex.pos.y * scale), int(vertex.pos.z * scale))
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
def run(dt):
    screen.fill((0, 0, 0))  # Clear screen with black
    triangles = [updateTriangle(t) for t in cube_vertices]  # Use the cube vertices defined above
    print(triangles)
    for t in triangles:
       
        draw_texture(t, texture)  # Load and draw texture
        drawTriangle(t, (255, 255, 255))  # Draw the triangle outline for visibility
        
    pygame.display.flip()  # Update the display
    return


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



        for y in range(y1, y2 + 1):
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

        for y in range(y2, y3 + 1):
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
