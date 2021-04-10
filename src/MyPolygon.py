# Simple polygon object. Stores vertices as a list of ordered tuples (x, y)
# Can return a list of edges, only if vertices are properly ordered
class Polygon():
    def __init__(self, vertices):
        self.vertices = vertices

    def getVertices(self):
        return self.vertices

    def getEdges(self):
        last = len(self.vertices)
        return [(self.vertices[x], self.vertices[(x+1)%last]) for x in range(0, last)]

# Simple line object. Too simple, not really used for anything.
class Line():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def getVars(self):
        return (self.a, self.b, self.c)