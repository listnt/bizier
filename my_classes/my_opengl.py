from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
class my_opengl(QGLWidget):

    def __init__(self, parent=None):
        super(my_opengl, self).__init__(parent)
        #orX = 2, orY = 5, trX = 0, trY = 0
        self.orX=32.0
        self.orY=80.0
        self.trX=0.0
        self.trY=0.0
        self.h=2.0
        self.ts = [t/100.0 for t in range(101)]
        self.data=[]
        self.points=[]
        

    def paintGL(self) :
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPolygonMode(GL_FRONT, GL_FILL)
        glLineWidth(2)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(-100.0, 0.0, 0.0)
        glVertex3f(100.0, 0.0, 0.0)
        glVertex3f(0.0, 100.0, 0.0)
        glVertex3f(0.0, -100.0, 0.0)
        for i in range(-100,101):
            glVertex3f(-1.6, 16*i, 0)
            glVertex3f(1.6, 16*i, 0)
            glVertex3f(i*6.4, -4, 0)
            glVertex3f(i*6.4, 4, 0)
        glEnd()
        if self.data:
            for l,i in zip(self.points,self.data):
                glColor3f(i["R"]/255.0,i["G"]/255.0,i["B"]/255.0)
                glLineWidth(i["Width"])
                glBegin(GL_LINE_STRIP)
                for p in l:
                    glVertex3f(p[0],p[1],0)
                glEnd()
        glFlush()
    def initializeGL(self) :
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.orX, self.orX, -self.orY, self.orY, -10, 10)

    def resizeGL(self,w,h):
        aspect = w / h
        glViewport(0, 0, w, h)
        glLoadIdentity()
        if (aspect >= 1.0):
            glOrtho((self.trX - self.orX)*aspect, (self.trX + self.orX)*aspect, 
            self.trY - self.orY, self.trY + self.orY, -10, 10)
            #print((self.trX - self.orX)*aspect, (self.trX + self.orX)*aspect, self.trY - self.orY, self.trY + self.orY)
        else:
            glOrtho(self.trX - self.orX, self.trX + self.orX, 
            (self.trY - self.orY)/aspect, (self.trY + self.orY)/aspect, -10, 10)
            #print((self.trY - self.orY)/aspect, (self.trY + self.orY)/aspect, self.trX - self.orX,self.trX + self.orX)

    def mousePressEvent(self,event):
        self.setFocus()
        
    def keyPressEvent(self,event):
        key = event.key()
        if (key == QtCore.Qt.Key_Left):
            self.trX -= 1 * self.orX / 4
            glLoadIdentity()
            glOrtho(self.trX - self.orX, self.trX + self.orX, 
            self.trY - self.orY, self.trY + self.orY, -10, 10)
        if (key == QtCore.Qt.Key_Right):
            self.trX += 1 * self.orX / 4 
            glLoadIdentity() 
            glOrtho(self.trX - self.orX, self.trX + self.orX, 
            self.trY - self.orY, self.trY + self.orY, -10, 10) 
        if (key == QtCore.Qt.Key_Up) :
            self.trY += 1 * self.orY / 10 
            glLoadIdentity() 
            glOrtho(self.trX - self.orX, self.trX + self.orX, 
            self.trY - self.orY, self.trY + self.orY, -10, 10) 
        if (key == QtCore.Qt.Key_Down) :
            self.trY -= 1 * self.orY / 10 
            glLoadIdentity() 
            glOrtho(self.trX - self.orX, self.trX + self.orX, 
            self.trY - self.orY, self.trY + self.orY, -10, 10) 
        if (key == QtCore.Qt.Key_Plus) :
            self.orX/=1.5
            self.orY/=1.5
            glLoadIdentity() 
            glOrtho(self.trX - self.orX, self.trX + self.orX, 
            self.trY - self.orY, self.trY + self.orY, -10, 10) 
        if (key == QtCore.Qt.Key_Minus) :
            self.orX*=1.5
            self.orY*=1.5
            glLoadIdentity() 
            glOrtho(self.trX - self.orX, self.trX + self.orX, 
            self.trY - self.orY, self.trY + self.orY, -10, 10) 
        if (key == QtCore.Qt.Key_Home) :
            self.trY = 0 
            self.trX = 0 
            self.orX = 2 
            self.orY = 5 
            glLoadIdentity() 
            glOrtho(self.trX - self.orX, self.trX + self.orX, 
            self.trY - self.orY, self.trY + self.orY, -10, 10)
        self.update()
        super().keyPressEvent(event)

    def update_data(self, data):
        self.data=data
        self.points=[]
        self.update()
        for l in data:
            bezier=self.make_bezier(numpy.column_stack((l["PointsX"],l["PointsY"])))
            self.points.append(bezier(self.ts))

    def make_bezier(self,points):
        n = len(points)
        combinations = self.pascal_row(n-1)
        def bezier(ts):
            result = []
            for t in ts:
                tpowers = (t**i for i in range(n))
                upowers = reversed([(1-t)**i for i in range(n)])
                coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
                result.append(
                    tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*points)))
            return result
        return bezier

    def pascal_row(self,n, memo={}):
        if n in memo:
            return memo[n]
        result = [1]
        x, numerator = 1, n
        for denominator in range(1, n//2+1):
            x *= numerator
            x /= denominator
            result.append(x)
            numerator -= 1
        if n&1 == 0:
            result.extend(reversed(result[:-1]))
        else:
            result.extend(reversed(result))
        memo[n] = result
        return result