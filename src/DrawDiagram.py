from PIL import Image, ImageDraw, ImageFont

import MyGeometry

# 'Constants' used for settings
FONT = ImageFont.truetype(font="arial.ttf", size=32)
X_MARGIN = 150 # Could be updated to account for label length...
Y_MARGIN = 64
TEXT_FLOAT = 20
DOMAIN = (2000, 2000) # Could be updated to account for input
ORIGIN = (0+X_MARGIN, DOMAIN[1]+Y_MARGIN)
RESOLUTION = (DOMAIN[0]+2*X_MARGIN, DOMAIN[1]+2*Y_MARGIN)

ELLIPSE_SIZE   = 10
MAINLINE_WIDTH = 10
MAINLINE_FILL  = "purple"

# Make the background of a cartesian plane
def generateGraph():

    graph = Image.new('RGBA', RESOLUTION, (0, 255, 0, 0))
    draw = ImageDraw.Draw(graph)

    # Y-axis
    draw.line([(ORIGIN[0], 0+Y_MARGIN), ORIGIN], fill="black", width=4)
    # X-axis
    draw.line([ORIGIN, (ORIGIN[0]+DOMAIN[0], ORIGIN[1])], fill="black", width=4)

    # Draw labels
    draw.text((ORIGIN[0]-draw.textlength("0", font=FONT), ORIGIN[1]), "0", font=FONT, fill="black")

    # X-axis labels
    for i in range(100, DOMAIN[0]+1, 100):
        cursor = (ORIGIN[0]+i, ORIGIN[1]+TEXT_FLOAT)
        draw.text((cursor[0]-(draw.textlength(str(i), font=FONT)/2), cursor[1]), str(i), font=FONT, fill="black")
        draw.line([(cursor[0]-1, ORIGIN[1]-(TEXT_FLOAT/2)), (cursor[0]-1, ORIGIN[1]+(TEXT_FLOAT/2))], fill="black", width=3)

    # Y-axis labels
    for i in range(100, DOMAIN[1]+1, 100):
        cursor = (ORIGIN[0], ORIGIN[1]-i)
        draw.text((cursor[0]-TEXT_FLOAT-(draw.textlength(str(i), font=FONT)), cursor[1]-(draw.textsize(str(i), font=FONT)[1]/2)), str(i), font=FONT, fill="black")
        draw.line([(cursor[0]-(TEXT_FLOAT/2), cursor[1]), (cursor[0]+(TEXT_FLOAT/2), cursor[1])], fill="black", width=3)


    return graph

def drawVertex(draw, v, fill="black", outline="black"):
    draw.ellipse([(ORIGIN[0]+v[0]-ELLIPSE_SIZE, ORIGIN[1]-v[1]-ELLIPSE_SIZE), (ORIGIN[0]+v[0]+ELLIPSE_SIZE, ORIGIN[1]-v[1]+ELLIPSE_SIZE)], fill=fill, outline=outline)

def connectVertices(draw, v1, v2, width=1, fill="black"):
    draw.line([(ORIGIN[0]+v1[0], ORIGIN[1]-v1[1]), (ORIGIN[0]+v2[0], ORIGIN[1]-v2[1])], width=width, fill=fill)

def drawLabel(draw, position, text, font=FONT, fill="black"):
    l = draw.textsize(text, font=FONT)
    position = (position[0]-(l[0]/2), position[1]+(l[1]/2))
    draw.text((ORIGIN[0]+position[0], ORIGIN[1]-position[1]), text, font=font, fill=fill)

# Needs to be fixed to account for string length
def getOrthogonalFloat(point, direction, float_v):
    if direction[0] == 0 and direction[1] == 0:
        return (point[0], point[1]+float_v)
    else:
        d_sum   = abs(direction[0])+abs(direction[1])
        x_coef  = direction[0]*direction[1]/(abs(direction[0]*direction[1]))
        x_ratio = abs(direction[1]/d_sum)*x_coef
        y_ratio = abs(direction[0]/d_sum)

        return (point[0]-(float_v*x_ratio), point[1]+(float_v*y_ratio))

def getParallelFloat(point, direction, float_v):
    d_sum = abs(direction[0])+abs(direction[1])
    x_ratio = direction[0]/d_sum
    y_ratio = direction[1]/d_sum

    return (point[0]+(float_v[0]*x_ratio), point[1]+(float_v[1]*y_ratio))


def drawMainLine(draw, line):
    if line[0] == 0:
        if line[1] == 0:
            return
        else:
            y_value = ORIGIN[1]-(line[2]/line[1])
            draw.line([(ORIGIN[0], y_value), (ORIGIN[0]+DOMAIN[0], y_value)], width=MAINLINE_WIDTH, fill=MAINLINE_FILL)
    
    elif line[1] == 0:
        x_value = ORIGIN[0] + (line[2]/line[0])
        draw.line([(x_value, ORIGIN[1]), (x_value, ORIGIN[1]-DOMAIN[1])], width=MAINLINE_WIDTH, fill=MAINLINE_FILL)

    else:
        intercepts = list()
        c_r = line[2]/line[1]
        x_r = -line[0]/line[1]
        y_d = DOMAIN[0]*x_r + c_r
        y_r = -line[1]/line[0]
        c_x = line[2]/line[0]
        x_d = DOMAIN[1]*y_r + c_x

        if 0 <= c_r <= DOMAIN[1]:
            intercepts.append((0, c_r))
        if 0 <= y_d <= DOMAIN[1]:
            intercepts.append((DOMAIN[0], y_d))
        if 0 <= c_x <= DOMAIN[0]:
            intercepts.append((c_x, 0))
        if 0 <= x_d <= DOMAIN[0]:
            intercepts.append((x_d, DOMAIN[0]))

        intercepts = set(intercepts)

        if len(intercepts) > 2:
            raise Exception("Line has more than 2 intercepts on rectangle?")

        if len(intercepts) == 2:
            draw.line([(v[0]+ORIGIN[0], ORIGIN[1]-v[1]) for v in intercepts], width=MAINLINE_WIDTH, fill=MAINLINE_FILL)


# Takes a "sunny side" solution and draws it on a graph.
def drawSolution(polygon, line, solution_set):
    diagram = generateGraph()
    sketch = ImageDraw.Draw(diagram)

    v_set = polygon.getVertices()

    #draw the poly gon and its vertices
    sketch.polygon([(ORIGIN[0]+v[0], ORIGIN[1]-v[1]) for v in v_set], fill="red", outline="black")

    for vertex in v_set:
        drawVertex(sketch, vertex, outline="white")

    drawMainLine(sketch, line)

    for vertex in solution_set[0]:
        drawVertex(sketch, vertex, fill="yellow")

    solution_point = solution_set[3]
    nearest_point  = MyGeometry.getNearestPointOnLine(solution_point, line)

    connectVertices(sketch, solution_point, nearest_point, width=10, fill="lime")

    drawVertex(sketch, solution_point, fill="lime")

    drawVertex(sketch, nearest_point, fill="lime")

    # Get label position for line
    mid_point = ((solution_point[0]+nearest_point[0])/2, (solution_point[1]+nearest_point[1])/2)
    d_vector = MyGeometry.getDirectionVector(solution_point, nearest_point)

    drawLabel(sketch, getOrthogonalFloat(mid_point, d_vector, 40), "Δ", fill="lime")

    # Draw labels for searched vertices
    center_point = MyGeometry.getCenterOfPolygon(polygon)
    i = 1

    for vertex in solution_set[4]:
        drawVertex(sketch, vertex, fill="blue")
        d_vector = MyGeometry.getDirectionVector(center_point, vertex)
        label = "[" + str(i) + "]"
        text_size = sketch.textsize(label, font=FONT)
        float_v = (TEXT_FLOAT+text_size[0], TEXT_FLOAT+text_size[1])

        drawLabel(sketch, getParallelFloat(vertex, d_vector, float_v), label, fill="blue")
        i += 1

    return diagram

def drawSolutionText(solution_set):
    msg = "Distance (Δ) = " + str(solution_set[1]) +"\n"
    msg += "Order of vertices searched: \n"

    search_list = solution_set[4]

    rows = 2

    for i in range(len(search_list)):
        msg += "[" + str(i+1) + "]: " + str(search_list[i]) + "\n"
        rows += 1

    msg_size = FONT.getsize(msg)

    notes_image = Image.new('RGBA', (RESOLUTION[0], (msg_size[1]*rows)+(Y_MARGIN*2)), (0, 255, 0, 0))
    draw = ImageDraw.Draw(notes_image)

    draw.text((X_MARGIN, Y_MARGIN), msg, fill="lime", font=FONT)

    return notes_image

def makeFile(new_polygon, new_line, solution_set, file_path=None):
    im = drawSolution(new_polygon, new_line, solution_set)
    im_2 = drawSolutionText(solution_set)

    final_im = Image.new('RGBA', (RESOLUTION[0], im.height+im_2.height), (0, 255, 0, 0))
    final_im.paste(im, (0, 0))
    final_im.paste(im_2, (0, im.height))

    if file_path == None:
        final_im.show()
    else:
        final_im.save(file_path, format='PNG')