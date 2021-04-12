import re as regex

# Takes in a file with a list of (x, y) coordinates and 
# a line in the form ax+by=c, and returns a list of 2-tuples
# and a 3-tuple representing a polygon and a line respectively
def readPolygonFile(open_file):

    input_text = open_file.read()

    data = [int(token) for token in regex.findall('-?[0-9]+', input_text)]

    if len(data) != data[0]*2 + 4:
        raise RuntimeError("Not enough arguments in file")

    vertices = list()

    for i in range(1, len(data)-3, 2):
        vertices.append((data[i], data[i+1]))

    line = (data[-3], data[-2], data[-1])

    return (vertices, line)