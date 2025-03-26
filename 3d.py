import pygame
import numpy as np
from pygame.locals import *

# Define vector and matrix structures
class Vec3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p = [p1, p2, p3]

class Mesh:
    def __init__(self):
        self.tris = []

class Mat4x4:
    def __init__(self):
        self.m = np.zeros((4, 4))

# Define 3D engine class
class Engine3D:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.width, self.height = width, height
        self.meshCube = Mesh()
        self.matProj = Mat4x4()
        self.fTheta = 0
        self.running = True
        self.create_mesh()
        self.create_projection()
    
    def create_mesh(self):
        self.meshCube.tris = [
            Triangle(Vec3D(0, 0, 0), Vec3D(0, 1, 0), Vec3D(1, 1, 0)),
            Triangle(Vec3D(0, 0, 0), Vec3D(1, 1, 0), Vec3D(1, 0, 0)),
            Triangle(Vec3D(1, 0, 0), Vec3D(1, 1, 0), Vec3D(1, 1, 1)),
            Triangle(Vec3D(1, 0, 0), Vec3D(1, 1, 1), Vec3D(1, 0, 1)),
            Triangle(Vec3D(1, 0, 1), Vec3D(1, 1, 1), Vec3D(0, 1, 1)),
            Triangle(Vec3D(1, 0, 1), Vec3D(0, 1, 1), Vec3D(0, 0, 1)),
            Triangle(Vec3D(0, 0, 1), Vec3D(0, 1, 1), Vec3D(0, 1, 0)),
            Triangle(Vec3D(0, 0, 1), Vec3D(0, 1, 0), Vec3D(0, 0, 0)),
        ]
    
    def create_projection(self):
        fNear, fFar, fFov = 0.1, 1000.0, 90.0
        fAspectRatio = self.height / self.width
        fFovRad = 1.0 / np.tan(np.radians(fFov / 2))
        
        self.matProj.m[0][0] = fAspectRatio * fFovRad
        self.matProj.m[1][1] = fFovRad
        self.matProj.m[2][2] = fFar / (fFar - fNear)
        self.matProj.m[3][2] = (-fFar * fNear) / (fFar - fNear)
        self.matProj.m[2][3] = 1.0
        self.matProj.m[3][3] = 0.0
    
    def multiply_matrix_vector(self, i, m):
        o = Vec3D()
        o.x = i.x * m.m[0][0] + i.y * m.m[1][0] + i.z * m.m[2][0] + m.m[3][0]
        o.y = i.x * m.m[0][1] + i.y * m.m[1][1] + i.z * m.m[2][1] + m.m[3][1]
        o.z = i.x * m.m[0][2] + i.y * m.m[1][2] + i.z * m.m[2][2] + m.m[3][2]
        w = i.x * m.m[0][3] + i.y * m.m[1][3] + i.z * m.m[2][3] + m.m[3][3]
        if w != 0:
            o.x /= w
            o.y /= w
            o.z /= w
        return o
    
    def update(self, dt):
        self.fTheta += dt
    
    def render(self):
        self.screen.fill((0, 0, 0))
        matRotZ, matRotX = Mat4x4(), Mat4x4()
        
        matRotZ.m[0][0] = np.cos(self.fTheta)
        matRotZ.m[0][1] = np.sin(self.fTheta)
        matRotZ.m[1][0] = -np.sin(self.fTheta)
        matRotZ.m[1][1] = np.cos(self.fTheta)
        matRotZ.m[2][2] = 1
        matRotZ.m[3][3] = 1
        
        matRotX.m[0][0] = 1
        matRotX.m[1][1] = np.cos(self.fTheta * 0.5)
        matRotX.m[1][2] = np.sin(self.fTheta * 0.5)
        matRotX.m[2][1] = -np.sin(self.fTheta * 0.5)
        matRotX.m[2][2] = np.cos(self.fTheta * 0.5)
        matRotX.m[3][3] = 1
        
        for tri in self.meshCube.tris:
            triProjected = Triangle(Vec3D(), Vec3D(), Vec3D())
            # triRotatedZ = Triangle(*[self.multiply_matrix_vector(p, matRotZ) for p in tri.p])
            triRotatedZX = Triangle(*[self.multiply_matrix_vector(p, matRotX) for p in tri.p])
            triTranslated = Triangle(*[Vec3D(p.x, p.y, p.z + 3) for p in triRotatedZX.p])
            triProjected = Triangle(*[self.multiply_matrix_vector(p, self.matProj) for p in triTranslated.p])
            
            for p in triProjected.p:
                p.x = (p.x + 1) * 0.5 * self.width
                p.y = (p.y + 1) * 0.5 * self.height
            
            pygame.draw.polygon(self.screen, (255, 255, 255), [(p.x, p.y) for p in triProjected.p], 1)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
            self.update(dt)
            self.render()
        pygame.quit()

if __name__ == "__main__":
    engine = Engine3D(800, 600)
    engine.run()
