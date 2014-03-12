#!/usr/bin/env python3

'''
this script has been taken from http://openglsamples.sourceforge.net/
modified to work with python3
it's an interesting example of use of openg with python
'''

import io, sys, numpy, math
from Lod import *
from Engine import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

import threading, time

tm = 0 # texmanager
lm = 0 # lodmanager
m = 0  # map
window = 0
gravity = True
fall = 1

sw = 1024  # glutGet(GLUT_WINDOW_WIDTH)
sh = 768
swf = float(sw) / 640.0
shf = float(sh) / 480.0

#camera
angle = 130.0
angle2 = 10.0
posx = 0
posy = 3000
posz = 0
lx = math.sin(math.radians(-angle))
lz = -math.cos(math.radians(-angle))
ly = math.sin(math.radians(-angle2))

sky_rot = 0.0

gobval = ('a', 'b', 'c', 'd', 'e', 'f')
gob = 0

def threadGob():
    global sky_rot,gob,gobval
    while True:
        time.sleep(.25)
        gob = (gob + 1) % 6

def threadInc():
    global sky_rot, posx, posz, posy, fall
    while True:
        time.sleep(.01)
        sky_rot = (sky_rot + 0.007) % 360.0

        if gravity:
            if (posy - 450) > m.TerrainHeight(posx, posz):
                fall += 1
                posy -= fall
            else:
                fall = 1
                posy = m.TerrainHeight(posx, posz) + 450

def ValidPos(ex,ez,ey):
    l = 44*512
    return ( -l < ex < l ) and ( -l < ez < l ) and (0 < ey < l/4)

def KeyPressed(*args):
    global posx,posy,posz,angle,angle2
    global lx,lz,ly, gravity

    rot_step = 8
    mov_step = 512*0.25

    if args[0] == b'\t': # tab
        angle = 130
        angle2 = 10
        posx = 0.
        posy = 0.
        posz = 0.

    if args[0] == b'\x1B': # escape
        sys.exit(0)

    if args[0] == b'\x7f':
        angle2 = (angle2 + rot_step) % 360
        if 80 < angle2 < 99:
            angle2 = 80
        ly = math.sin(math.radians(-angle2))

    if args[0] == 107:
        angle2 = 10
        ly = math.sin(math.radians(-angle2))

    if args[0] == 105:
        angle2 = (angle2 - rot_step) % 360
        if 100 < angle2 < 300:
            angle2 = 300
        ly = math.sin(math.radians(-angle2))

    if args[0] == b'g':
        gravity = not gravity

    if args[0] == b'a':
        angle = (angle + rot_step) % 360
        lx = math.sin(math.radians(-angle))
        lz = -math.cos(math.radians(-angle))

    if args[0] == b'd':
        angle = (angle - rot_step) % 360
        lx = math.sin(math.radians(-angle))
        lz = -math.cos(math.radians(-angle))

    if args[0] == b'w':
        ex = posx + mov_step * lx
        ez = posz + mov_step * lz
        if ValidPos(ex,ez,posy):
            posx = ex
            posz = ez

    if args[0] == b's':
        ex = posx - mov_step * lx
        ez = posz - mov_step * lz
        if ValidPos(ex,ez,posy):
            posx = ex
            posz = ez

    if args[0] == 104:
        ey = posy + mov_step/2
        if ValidPos(posx,posz,ey):
            posy = ey

    if args[0] == 108:
        ey = posy - mov_step/2
        if ValidPos(posx,posz,ey):
            posy = ey

def DrawBox(x,y,z, scale):
    glBindTexture(GL_TEXTURE_2D, tm.textures["cbsm"]['id']);
    glPushMatrix();
    glTranslatef(x,y,z)
    glEnable(GL_DEPTH_TEST)
    glScaled(scale,scale,scale);
    glBegin(GL_QUADS);
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
    glEnd();
    glPopMatrix();

def DrawSky(): # TODO put in OdmMap
    glBindTexture(GL_TEXTURE_2D, tm.textures["sky07"]['id']);
    glPushMatrix();
    glScaled(60000,60000,60000);
    glRotatef(sky_rot, 0.0, 1.0, 0.0);
    glBegin(GL_QUADS);
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
    glEnd();
    glPopMatrix();

def DrawAxis():
    l=512
    l2=512+50

    glPushMatrix();
    #glDisable(GL_COLOR_MATERIAL)
    #glDisable(GL_LIGHTING)
    #glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    glLineWidth(2.0);
    glBegin(GL_LINES);
    glColor3f(1,0,0);
    glVertex3f(0, 0, 0);
    glVertex3f(l, 0, 0);
    glColor3f(0,1,0);
    glVertex3f(0, 0, 0);
    glVertex3f(0, l, 0);
    glColor3f(0,0,1);
    glVertex3f(0, 0, 0);
    glVertex3f(0, 0, l);
    glEnd();
    # WARNING this causes a segfault on exit on my machine
    #glColor3f(1.0, 1.0, 0.2)
    #glRasterPos3f(l2, 0.0, 0.0)
    #glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord('x'))
    #glRasterPos3f(0.0, l2, 0.0)
    #glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord('y'))
    #glRasterPos3f(0.0, 0.0, l2)
    #glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord('z'))
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glPopMatrix();

def DrawText(msg):
    glPushMatrix();
    #glDisable(GL_COLOR_MATERIAL)
    #glDisable(GL_LIGHTING)
    glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    hoff = sh - shf*(tm.textures["border2.pcx"]['h'] + 5)

    off = 0
    glColor3f(1, 1, 1)
    for c in msg:
        off += 9
        glRasterPos2f(18 + off, hoff)
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
    glEnable(GL_TEXTURE_2D)
    glPopMatrix();

def Draw2DImage(texture, w, h, x, y):
    global swf,shf
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture)
    glTranslatef(x,y,0)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0); glVertex2f(0.0, 0.0)
    glTexCoord2f(0.0, 0.0); glVertex2f(0.0, h*shf)
    glTexCoord2f(1.0, 0.0); glVertex2f(w*swf, h*shf)
    glTexCoord2f(1.0, 1.0); glVertex2f(w*swf, 0.0)
    glEnd()
    glPopMatrix()

def DrawSprite(texture, w, h, x, y, z, scale): #TODO future Sprite,SpriteManager class
    glPushMatrix()
    glEnable(GL_DEPTH_TEST)
    glBindTexture(GL_TEXTURE_2D, texture) # this would be a texture relative to the angle between camera and sprite rotation.
    r = float(h)/float(w)
    glTranslatef(x, y, z)
    glScaled(scale,scale,scale)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.0, 0.0,0.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.0, 1.0*r,0.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.0, 1.0*r,0.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(1.0, 0.0,0.0)
    glEnd()
    glPopMatrix()

def InitGL():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    #glClearDepth(1.0)
    glDepthFunc(GL_LESS) # LEQUAL
    glShadeModel(GL_SMOOTH) # FLAT
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    #glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);

def Set2DMode():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, sw, sh)
    glOrtho(0, sw, sh, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    glEnable (GL_BLEND)
    glBlendFunc ( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def SetMiniMapMode():
    global posx,posy,posz, lx,lz,ly, sw, sh
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    w = 200
    glViewport(sw-w, sh-2*w, w, w)
    #gluPerspective(50.0, 1.0, 512, 512*1000)
    #glFrustum(0,w,w,0,1.,10.)
    glOrtho(3,1,3,1,1,3);
    #glOrtho(0,256,256,0,-1,1)
    #gluLookAt(
    #    0,2,0,
    #    0,0,0,
    #    0,0,-1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    #glEnable (GL_BLEND)
    #glBlendFunc ( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glClearColor(.3, 1.0, .3, 0.0)

def Set3DMode(w,h):
    global posx,posy,posz, lx,lz,ly, sw, sh
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, h, sw - w, sh-h)
    gluPerspective(45.0, float(sw) / float(sh), 1, 512*250)
    gluLookAt(posx, posy, posz,
              posx + lx, posy + ly, posz + lz,
              0.0, 1.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity();
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    #glDisable(GL_COLOR_MATERIAL)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    '''
    lightAmbient = [0.2, 0.3, 0.6, 1.0]
    lightDiffuse = [0.2, 0.3, 0.6, 1.0]
    lightPosition = [0,1000,600,1]

    glEnable(GL_LIGHTING);
    glLightfv(GL_LIGHT0, GL_AMBIENT,lightAmbient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuse)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
    glEnable(GL_LIGHT0)
    '''
def Render():
    global m,swf,shf
    global gobval,gob
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    max_w = int((tm.textures["border1.pcx"]['w']) * swf)
    max_h = int((tm.textures["footer"]['h'] + tm.textures["border2.pcx"]['h'] - 5) * shf)
    Set3DMode(max_w, max_h)
    DrawSky()

    m.Draw()
    m.DrawGameArea()
    DrawBox(-2000,m.TerrainHeight(-1000, 1000)+10,1500, 90)
    t = tm.textures["gobfi{}0".format(gobval[gob])]
    DrawSprite(t['id'], t['w'], t['h'], -1000.0,m.TerrainHeight(-1000, 1000)+10,1000, 512 )

    SetMiniMapMode()
    m.Draw()

    DrawAxis()
    Set2DMode()

    t = tm.textures["footer"]
    Draw2DImage(t['id'], t['w'], t['h'],
                0.0,
                (sh - shf*(float(tm.textures["border2.pcx"]['h']+t['h'] - 5)) ) )

    t = tm.textures["border2.pcx"] # there is a problem in pillow library for this image (fixed in git version of pillow)
    Draw2DImage(t['id'], t['w'], t['h'], 0.0, sh - shf*float(t['h']))

    t = tm.textures["border1.pcx"]
    Draw2DImage(t['id'], t['w'], t['h'],
               (sw-swf*float(t['w'])) , (sh - shf*float(t['h'])) )

    t = tm.textures["border3"]
    Draw2DImage(t['id'], t['w'], t['h'], 0.0, 0.0)

    t = tm.textures["border4"]
    Draw2DImage(t['id'], t['w'], t['h'], 0.0, 0.0)

    t = tm.textures["tap2"]
    Draw2DImage(t['id'], t['w'], t['h'], sw - swf*float(t['w']), 0.0)

    t = tm.textures["malea01"]
    Draw2DImage(t['id'], t['w'], t['h'], swf*22.0, shf*383.0)

    t = tm.textures["eradcate"]
    Draw2DImage(t['id'], t['w'], t['h'], swf*135.0, shf*383.0) # distance ~113px

    #segfault
    DrawText("pos ({0:.2f},{1:.2f},{2:.2f}) ang ({3:.2f} {4:.2f}). [TAB] toggle testroom".format(posx,posy,posz,angle, angle2))

    glutSwapBuffers()

def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(sw,sh)
    glutInitWindowPosition(200,200)
    window = glutCreateWindow(b'Openmm_engine test')

    global lm, tm
    lm = LodManager()
    lm.LoadLods('data')
    tm = TextureManager(lm)
    tm.LoadTexture ("icons", "mm6title.pcx")
    tm.LoadTexture ("bitmaps", "bemob2b") # wall
    tm.LoadTexture ("bitmaps", "d2ceil4") # ceil
    tm.LoadTexture ("bitmaps", "bcsctr")  # floor
    tm.LoadTexture ("bitmaps", "cbsm")
    tm.LoadTexture ("bitmaps", "sky07")
    tm.LoadTexture ("icons", "border1.pcx")
    tm.LoadTexture ("icons", "border2.pcx")
    tm.LoadTexture ("icons", "border3")
    tm.LoadTexture ("icons", "border4")
    tm.LoadTexture ("icons", "tap2", (255,0,0)) # specific alpha color
    tm.LoadTexture ("icons", "footer")
    tm.LoadTexture ("icons", "eradcate")
    tm.LoadTexture ("icons", "malea01")
    tm.LoadTexture ("sprites08", "gobfia0", True) # true get first pixel for alpha
    tm.LoadTexture ("sprites08", "gobfib0", True)
    tm.LoadTexture ("sprites08", "gobfic0", True)
    tm.LoadTexture ("sprites08", "gobfid0", True)
    tm.LoadTexture ("sprites08", "gobfie0", True)
    tm.LoadTexture ("sprites08", "gobfif0", True)

    global m
    if len(sys.argv) > 1:
        m = OdmMap("out{}.odm".format(sys.argv[1]), lm, tm)
    else:
        m = OdmMap("oute3.odm", lm, tm)

    glutDisplayFunc(Render)
    glutIdleFunc(Render)
    glutKeyboardFunc(KeyPressed) # glutKeyboardUpFunc
    glutSpecialFunc(KeyPressed)
    InitGL()

    t1 = threading.Thread(target=threadInc)
    t1.daemon = True
    t1.start()

    t2 = threading.Thread(target=threadGob)
    t2.daemon = True
    t2.start()

    glutMainLoop()

if __name__ == "__main__":
    main()
