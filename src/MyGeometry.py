import math

# Returns the shortest distance from a point to a line as a float
def pointLineDistance(point, line):
    return abs((point[0]*line[0]+point[1]*line[1]-line[2])/(math.sqrt(line[0]**2 + line[1]**2)))

# Returns the center of a give polygon as a tuple (x, y)
def getCenterOfPolygon(polygon):
    return getCenterOfVertices(polygon.getVertices())

# Returns the center of a set of vertices as a tuple (x, y)
def getCenterOfVertices(vertices):
    divisor, x_sum, y_sum = (0, 0, 0)
    
    for x, y in vertices:
        x_sum += x
        y_sum += y
        divisor += 1

    return (x_sum/divisor, y_sum/divisor)

# Returns the reciprocal of a real number as a float
def reciprocal(val):
    if val != 0:
        return 1.0/val
    
    return val

# Returns the projection of a point onto a line in the form (ax+by=c)
def projectPointOnLine(point, line):
    a = reciprocal(line[0])
    b = -reciprocal(line[1])

    c = a*point[0] + b*point[1]

    return (a, b, c)

# Returns the intersect of two lines as a tuple (x, y)
def findIntersect(line_1, line_2):
    r = line_1[0]/line_2[0]
    c_prime = line_1[2]-r*line_2[2]
    
    y = c_prime/(line_1[1]-r*line_2[1])
    x = (line_1[2]-y*line_1[1])/line_1[0]

    return (x, y)

# Returns the nearest point on a line to another point as a tuple (x, y)
def getNearestPointOnLine(point, line):
    return findIntersect(line, projectPointOnLine(point, line))

# Returns the directional vector from one point to another as a tuple (x', y')
def getDirectionVector(start, terminal):
    return (terminal[0]-start[0], terminal[1]-start[1])