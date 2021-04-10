from MyPolgyon import Polygon
import MyGeometry

def getXY():
    return (1, 2)

x,y = getXY()

print("x=" + str(x))
print("y=" + str(y))
print("Distance from 3x+5y=2: " + str(MyGeometry.pointLineDistance((3,5,2), getXY())))