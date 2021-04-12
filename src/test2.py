import MyPolygon
import MyGeometry
import MyCollision

vertex_list = list()

x = 7
y = 1.5
vertex_list.append((x, y))

for i in range(5):
    x += 0.2
    y -= 0.1
    vertex_list.append((x, y))
    

for i in range(5):
    x += 0.2
    y += 0.1
    vertex_list.append((x, y))

for i in range(5):
    x -= 0.2
    y += 0.1
    vertex_list.append((x, y))

for i in range(4):
    x -= 0.2
    y -= 0.1
    vertex_list.append((x, y))

new_polygon = MyPolygon.Polygon(vertex_list)
new_line = (-1, 10, 0)

solution = MyCollision.bruteForceDistance(new_polygon, new_line)

print("Solution:(distance, index, vertex)=" + str(solution))
print("Nearest point on new_line to solution: " + str(MyGeometry.getNearestPointOnLine(solution[2], new_line)))
print("Projection of solution on line: " + str(MyGeometry.projectPointOnLine(solution[2], new_line)))

center = MyGeometry.getCenterOfPolygon(new_polygon)
print("Center: " + str(center))
icenter = MyGeometry.getNearestPointOnLine(center, new_line)

print("Direction Vector: " + str(MyGeometry.getDirectionVector(center, icenter)))

sunny_side = MyCollision.getSunnySideOf(new_polygon, new_line)

print("Sunny side solution of new_polygon: ([sunny_side], distance, index, (vertex), (search_order))\n" + str(MyCollision.sunnySearchSolution(sunny_side, new_line)))