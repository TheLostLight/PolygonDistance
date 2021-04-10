from PIL import Image, ImageDraw, ImageFont

# 'Constants' used for settings
FONT = ImageFont.truetype(font="arial.ttf", size=32)
X_MARGIN = 150
Y_MARGIN = 64
TEXT_FLOAT = 20
DOMAIN = (2000, 2000)
ORIGIN = (0+X_MARGIN, DOMAIN[1]+Y_MARGIN)
RESOLUTION = (DOMAIN[0]+2*X_MARGIN, DOMAIN[1]+2*Y_MARGIN)

ELLIPSE_SIZE = 10

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

def drawVertex(draw, v, fill="black", label=None, pos=None):
    draw.ellipse([(v[0]-ELLIPSE_SIZE, v[1]-ELLIPSE_SIZE), (v[0]+ELLIPSE_SIZE, v[1]+ELLIPSE_SIZE)], fill=fill)

    if label != None and pos != None:
        pass #Draw label if given

im = generateGraph()
im.show()