import math

def pointLineDistance(line, point):
    return (point[0]*line[0]+point[1]*line[1]-line[2])/(math.sqrt(line[0]**2 + line[1]**2))