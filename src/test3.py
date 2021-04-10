from PIL import Image, ImageDraw

import MyGeometry
from MyPolygon import Polygon
import MyCollision

result = Image.new('RGBA', (2000, 2000), (0, 255, 0, 0))
draw = ImageDraw.Draw(result)

new_polygon = Polygon([(700, 900), (600, 1000), (500, 900), (400, 800), (400, 700), (400, 600), (500, 500), (600, 400), (700, 500), (800, 600), (800, 700), (800, 800)])
new_line = (-5, 1, -5000)

draw.line([(1000, 0), (1400, 2000)], width=10, fill="purple")
for e in new_polygon.getEdges():
    draw.line([*e], fill="blue", width=5)

for v in new_polygon.getVertices():
    draw.ellipse([(v[0]-10, v[1]-10), (v[0]+10, v[1]+10)], fill="red")

sunny_side = MyCollision.getSunnySideOf(new_polygon, new_line)

for v in sunny_side:
    draw.ellipse([(v[0]-10, v[1]-10), (v[0]+10, v[1]+10)], fill="yellow")

solution = MyCollision.sunnySearchSolution(sunny_side, new_line)

nearestp = MyGeometry.getNearestPointOnLine(solution[2], new_line)

draw.ellipse([(nearestp[0]-10, nearestp[1]-10), (nearestp[0]+10, nearestp[1]+10)], fill="yellow")

draw.line([solution[2], nearestp], width=2, fill="green")

coords = ((solution[2][0] + nearestp[0])/2, (solution[2][1] + nearestp[1])/2 + 10)

draw.text(coords, "Distance=" + str(solution[0]), fill="green")

result.show()