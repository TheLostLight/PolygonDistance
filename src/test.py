from MyPolygon import Polygon
import MyGeometry

def getXY():
    return (1, 2)

x,y = getXY()

p = Polygon(((0,0), (4,0), (4,4), (0,4)))

print("x=" + str(x))
print("y=" + str(y))
print("Distance from 3x+5y=2: " + str(MyGeometry.pointLineDistance(getXY(), (3,5,2))))
print("Distance from (9, 2) to x-y=0: " + str(MyGeometry.pointLineDistance((0, 7), (1, -1, 0))))
print("Center of p: " + str(MyGeometry.getCenterOfPolygon(p.getVertices())))
c_point = (3, 4)
l = (3, 2, 3)
l_prime = MyGeometry.projectPointOnLine(c_point, l)
l_intersect = MyGeometry.findIntersect(l, l_prime)
print("Projection of " + str(c_point) +  " on " + str(l) + ": " + str(l_prime))
print("Intersect of " + str(l_prime) + " and " + str(l) + ": " + str(l_intersect))
print("Direction vector of " + str(c_point) + " and " + str(l_intersect) + ": " + str(MyGeometry.getDirectionVector(c_point, l_intersect)))