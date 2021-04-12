import random
import math

# Referenced https://cglab.ca/~sander/misc/ConvexGeneration/convex.html
# Viewed April 8, 2021, 19:30
def generatePolygon(n_vertices, scale):
    x_list = [random.randint(scale[0], scale[1]) for _ in range(n_vertices)]
    y_list = [random.randint(scale[2], scale[3]) for _ in range(n_vertices)]

    x_list.sort()
    y_list.sort()

    x_min = x_list[0]
    x_max = x_list[-1]
    y_min = y_list[0]
    y_max = y_list[-1]

    x_1 = [x_min]
    x_2 = [x_min]
    y_1 = [y_min]
    y_2 = [y_min]

    for i in range(1, len(x_list)-1):
        if random.randint(0, 1) > 0:
            x_1.append(x_list[i])
        else:
            x_2.append(x_list[i])
        if random.randint(0, 1) > 0:
            y_1.append(y_list[i])
        else:
            y_2.append(y_list[i])

    x_1.append(x_max)
    x_2.append(x_max)
    y_1.append(y_max)
    y_2.append(y_max)

    x_vec = list()
    y_vec = list()

    for i in range(len(x_1)-1):
        x_vec.append(x_1[i+1]-x_1[i])
    for i in range(len(x_2)-1):
        x_vec.append(x_2[i]-x_2[i+1])
    for i in range(len(y_1)-1):
        y_vec.append(y_1[i+1]-y_1[i])
    for i in range(len(y_2)-1):
        y_vec.append(y_2[i]-y_2[i+1])
        
    random.shuffle(y_vec)

    vectors = [(x_vec[i], y_vec[i]) for i in range(n_vertices)]

    vectors.sort(key=getVectorDegree)

    next_x = 0
    next_y = 0
    min_polygon_x = 0
    min_polygon_y = 0

    vertices = list()

    for i in range(n_vertices):
        vertices.append((next_x, next_y))

        next_x += vectors[i][0]
        next_y += vectors[i][1]

        min_polygon_x = min(next_x, min_polygon_x)
        min_polygon_y = min(next_y, min_polygon_y)

    x_shift = x_min - min_polygon_x
    y_shift = y_min - min_polygon_y

    polygon = list()

    for i in range(n_vertices):
        polygon.append((vertices[i][0]+x_shift, vertices[i][1]+y_shift))

    return polygon

def getVectorDegree(vector):
    return math.atan2(vector[1], vector[0])

def printRandomPolygonToFile(open_file, n_vertices, boundary):
    open_file.write("#-of vertices: " + str(n_vertices) + "\n\n")

    vertex_list = generatePolygon(n_vertices, boundary)
    
    open_file.write(str(vertex_list) + "\n")