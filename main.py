#implementation of point in triangle formula
import math
from PIL import Image

img = Image.new("RGB", (255, 255), "black")
px = img.load()

class vector2:
    def __init__(self, x:float, y:float):
        self.e = [x, y] #set x and y of vector in array

    def __add__(self, other):
        return vector2(self.x() + other.x(), self.y() + other.y()) #add x and y components and put in new 2 component vector

    def __sub__(self, other):
        return vector2(self.x() - other.x(), self.y() - other.y()) #subtract x and y components and put in new 2 component vector

    def __mul__(self, other):
        #check if other component is a vector
        if type(other) == vector2:
            return vector2(self.x() * other.x(), self.y() * other.y())  #yes, multiply both components individually
        else:
            return vector2(self.x() * other, self.y() * other) #no, multiply both by same number
    
    def __truediv__(self, other):
        #check if other component is vector
        if type(other) == vector2:
            return vector2(self.x() / other.x(), self.y() / other.y()) #yes, divide both components seperately
        else:
            return vector2(self.x() / other, self.y() / other) #no, divide both by same number

    def length_squared(self):
        return (self.x() ** 2) + (self.y() ** 2) #a^2 + b^2 = c^2
    
    def length(self):
        return math.sqrt(self.length_squared()) #c = sqrt(c^2)

    def x(self):
        return self.e[0] #return x component of array

    def y(self):
        return self.e[1] #return y component of array

class triangle:
    def __init__(self, p1:vector2, p2:vector2, p3:vector2):
        self.p = [p1, p2, p3]
    
    def getWValues(self, p:vector2):
        w1 = ((self.a().x() * (self.c().y() - self.a().y()))  +  ((p.y() - self.a().y()) * (self.c().x() - self.a().x()))  -  (p.x() * (self.c().y() - self.a().y())))   /   (((self.b().y() - self.a().y()) * (self.c().x() - self.a().x()))  -  ((self.b().x() - self.a().x()) * (self.c().y() - self.a().y())))
        w2 = (p.y() - self.a().y() - (w1 * (self.b().y() - self.a().y()))) / (self.c().y() - self.a().y())
        return vector2(w1, w2)

    def isInTriangle(self, p:vector2):
        wvals = self.getWValues(p) #get both w values in vector

        w1 = wvals.x()  #get w1 out of vector
        w2 = wvals.y()  #get w2 out of vector

        if w1 + w2 > 1: return False #combined w1 and w2 > 0 means outside triangle
        if w1 < 0 or w2 < 0: return False #numbers smaller than 0 means outside triangle
        return True

    def wToXY(self, wvals:vector2):
        #get w1 and w2 out of vector for ease of use in next step
        w1 = wvals.x()
        w2 = wvals.y()

        #find x and y point corresponding to w1 and w2 in triangle
        px = self.a().x() + (w1 * (self.b().x() - self.a().x())) + (w2 * (self.c().x() - self.a().x()))
        py = self.a().y() + (w1 * (self.b().y() - self.a().y())) + (w2 * (self.c().y() - self.a().y()))
        return vector2(px, py)

    #get point a
    def a(self):
        return self.p[0]

    #get point b
    def b(self):
        return self.p[1]
    
    #get point c
    def c(self):
        return self.p[2]

UVTriangle = triangle(vector2(193, 746), vector2(590, 52), vector2(988, 745))    #specify triangle in cat image
tris = [
    triangle(vector2(121, 336)*4, vector2(118, 186)*4, vector2(285, 338)*4), #cube front triangle bottom
    triangle(vector2(118, 186)*4, vector2(286, 188)*4, vector2(285, 338)*4), #cube front triangle top
    triangle(vector2(118, 186)*4, vector2(182, 144)*4, vector2(286, 188)*4), #cube top triangle bottom
    triangle(vector2(182, 144)*4, vector2(337, 146)*4, vector2(286, 188)*4), #cube top triangle top
    triangle(vector2(285, 338)*4, vector2(286, 188)*4, vector2(403, 337)*4), #slope front face
    triangle(vector2(286, 188)*4, vector2(337, 146)*4, vector2(403, 337)*4), #slope angled part bottom
    triangle(vector2(337, 146)*4, vector2(452, 276)*4, vector2(403, 337)*4)  #slope angled part top
] #triangles in image that need the cat texture

cat = Image.open("./cat.png", "r") #load cat image
catTEX = cat.load() #turn cat image into pixel array

img = Image.new("RGB", (2048, 2048), "black") #make output image
px = img.load() #make pixels array for output image

#go over all pixels in image
for y in range(2048):    
    for x in range(2048):
        #make 2 component vector as a point for next functions
        point = vector2(x, y)
        for tri in tris:    #go over all triangles in scene
            if tri.isInTriangle(point): #check if current point is in current triangle
                cw = tri.getWValues(point)  #get w1 and w2 if point is in triangle
                cpos = UVTriangle.wToXY(cw) #get position on the cat image
                px[x, y] = catTEX[cpos.x(), cpos.y()] #set color to corresponding position on the cat image

img.save("./cat_uvmapped.png") #save image