from math import *

class Vertex():
    x = 0.0
    y = 0.0

    def Vertex(self, x,y):
        self.x = x
        self.y = y

    def distance(self, b):
        a2 = self.x - b.x
        b2 = self.y = b.y
        return sqrt(a2*a2+b2*b2)

    def findRanges(self, vertices):
        return sorted([self.distance(x): x for x in vertices])

class Edge():
    a = 0
    b = 0

    def Edge(self, a, b):
        self.a = a
        self.b = b

    def dotProduct(self, b):
        return self.a * b.a + self.b * b.b

    def length(self):
        return self.a.distance(self.b)

    def __add__(self, x):
        return Edge(self.a + x.a, self.b + x.b)

    def __sub__(self, x):
        return Edge(self.a - x.a, self.b - x.b)

    def __neg__(self):
        return Edge(-self.a, -self.b)

    def __mul__(self, k):
        return Edge(self.a * k, self.b * k)

    def __div__(self, k):
        return self * (1/k)

    def unitVector(self):
        return self / self.length()

    def projectTo(self, e):
        return self.unitVector() * (self.dotProduct(e)
                                    / self.length())

    def pointAt(self, x):
        return (self - x.projectTo(self))

    def normal(self, x):
        return (self.pointAt(x)).unitVector()

    def findClosestOuter(self, tip, vertices):
        best = None
        best_dist = None

        tip_vec = self.normal(tip)

        for v in vertices:
            dot = tip_vec.dotProduct(v)
            if (dot > 0):
                dist = self.pointAt(v).length()
                if (best is None) or (dist < best_dist):
                    best = v
                    best_dist = dist

        return best

class Polygon():
    vertices = []

    def Polygon(self, vs):
        # vertices in `vs' are GridRef s
        self.vertices = [Vertex(float(gr.x),
                                float(gr.y)) for gr in vs]

    def defineSelf(self):
        if len(vertices) < 3:
            return              # not possible

        tri = [self.vertices[0]].extend(
            self.vertices[0].findRanges(self.vertices[1:]))[:3]

        triEdges = [Edge(tri[0], tri[1]),
                    Edge(tri[1], tri[2]),
                    Edge(tri[2], tri[0])]

        for edge in triEdges:
            

def polyGen(coords):
    # `coords' is a list of grid refs
    poly = Polygon(coords)
    
    
    
