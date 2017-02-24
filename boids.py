from itertools import combinations, product
import math
from OpenGL.GL import shaders
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, \
                                                      glBindVertexArray
import logging
from OpenGL.arrays import vbo
from ctypes import *
import numpy as np
import time
from random import random

logging.basicConfig()
log = logging.getLogger()
log.level=10

PARTICLE_COUNT=100
window = None
shader=None

step = 0
P_COUNT_F=float(PARTICLE_COUNT)
start = 0

SIZE=0.05
SIGHT=0.1
AVOID=0.05

_SIGHT=None
_AVOID=None

particles = np.array([[random()-0.5,random()-0.5, random()-0.5, 0, 0, 0] for _ in xrange(PARTICLE_COUNT)])


def main():

    global start
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
    glutInitWindowSize(1024,1024)
    glutInitWindowPosition(0, 0)
    window=glutCreateWindow("Boids")
    init()
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    start = time.time()
    glutMainLoop()


def init():
    global _SIGHT
    global _AVOID
    
    _SIGHT=SIGHT**2
    _AVOID=AVOID**2
    
    glClearColor(0.0,0,0.0,1.0)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glColorMaterial ( GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE );
    glEnable ( GL_COLOR_MATERIAL );


    
    glMatrixMode (GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective (40.0, 1.0, 0.1, 1500.0)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0.0,0.0,-1.0)

def update():
    for i in xrange(PARTICLE_COUNT):
        p1=particles[i]
        neighbors=[]
        for j in xrange(i+1,PARTICLE_COUNT):

            p2=particles[j]

            direction = ((p2[0]-p1[0])**2,
                         (p2[1]-p1[1])**2,
                         (p2[2]-p1[2])**2)

            
            sqrdist = sum(direction)
            
            if(sqrdist>_SIGHT):
                continue

            neighbors.append(direction)
        
        aim = [0,0,0]

        center=[0,0,0]
        
        for neighbor in neighbors:
            center[0]+=neighbor[0]
            center[1]+=neighbor[1]
            center[2]+=neighbor[2]

            diff = []
            dist = 0
            for i in xrange(3):
                diff.append(p1[i]-neighbor[i])
                dist+=diff[-1]**2

            if sum(diff)<_AVOID:
                aim[0]-=(_AVOID-diff[0])/1000
                aim[1]-=(_AVOID-diff[1])/1000
                aim[2]-=(_AVOID-diff[2])/1000

        if neighbors:    
            center = [center[0]/len(neighbors),center[1]/len(neighbors),center[2]/len(neighbors)]

        speed = 0
            
        for dim in xrange(3):
            aim[dim]+=(center[dim]-p1[dim])/((10.0*len(neighbors))or 1)
            p1[dim+3]+=aim[dim]
            speed += p1[dim+3]**2

        speed = math.sqrt(speed) or 1

        p1[3] = (p1[3]/speed)*0.005
        p1[4] = (p1[4]/speed)*0.005
        p1[5] = (p1[5]/speed)*0.005
        
        for dim in xrange(3):
            p1[dim]+=p1[dim+3]            
            
            

def draw():
    global step
    step+=1
    update()

    if random()<0.01:
        log.info(" FPS: {}".format(float(step)/(time.time()-start)))
    

    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)


    glColor3f(0.3, 0.8, 1.0)
    glBegin(GL_LINES)
    
    for particle in particles:

        glVertex3f(particle[0]-particle[3],particle[1]-particle[4],particle[2]-particle[5])
        glVertex3f(particle[0]+particle[3],particle[1]+particle[4],particle[2]+particle[5])

        
    glEnd()

    glFlush()
    

if __name__=='__main__':
    main()
