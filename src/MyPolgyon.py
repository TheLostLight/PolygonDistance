class Polygon():
    def __init__(self, vertices):
        self.vertices = vertices

    def getVertices(self):
        return self.vertices

    def getEdges(self):
        last = len(self.vertices)
        return [(self.vertices[x], self.vertices[(x+1)%last]) for x in range(0, last)]

class Line():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def getVars(self):
        return (self.a, self.b, self.c)