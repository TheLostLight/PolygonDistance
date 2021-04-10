import MyGeometry
from operator import lt as isLessThan, le as isLessOrEqualTo, gt as isGreaterThan, ge as isGreaterOrEqualTo

# Returns the vertices of the polygon that make up the sunny side with
# respect to the given line, as a list of tuples (x, y)
def getSunnySideOf(polygon, line):
    # Find the direction of the line from the polygon
    center = MyGeometry.getCenterOfPolygon(polygon) # Maybe this can be replaced by any arbitrary vertex in the polygon?
    projection = MyGeometry.projectPointOnLine(center, line)
    intersect = MyGeometry.findIntersect(line, projection)
    direction = MyGeometry.getDirectionVector(center, intersect)

    # The directional vector tells us which axis to compare first
    axis = 1 if abs(direction[0]) > abs(direction[1]) else 0
    scnd = int(not axis)

    # Need to know which quadrant to look for
    comparators = getComparators(bool(scnd), direction[scnd] > 0)

    # Prepare loop vars
    full_set = polygon.getVertices()
    end = len(full_set)
    i = 0
    sunny_side = list()

    # Loop through the vertices, find the starting and
    # ending point of desired quadrant
    while True:
        if comparators[0](full_set[i][axis], full_set[(i+1)%end][axis]):
            if comparators[1](full_set[(i-1)%end][axis], full_set[i][axis]):
                while comparators[0](full_set[i][axis], full_set[(i+1)%end][axis]):
                    sunny_side.append(full_set[i])
                    i = (i+1)%end
                sunny_side.append(full_set[i])
                return sunny_side
            else:
                i -= 1

        else:
            i = (i+1)%end

def getComparators(isYaxis, isPositive):
    if isYaxis:
        if isPositive:
            return (isGreaterThan, isLessOrEqualTo)
        else:
            return (isLessThan, isGreaterOrEqualTo)
    else:
        if isPositive:
            return (isLessThan, isGreaterOrEqualTo)
        else:
            return (isGreaterThan, isLessOrEqualTo)

# Binary search for vertex distances
def sunnySearchSolution(sunny_side, line):
    left      = 0
    right     = len(sunny_side)-1
    partition = int((left+right)/2)
    mid_dist  = MyGeometry.pointLineDistance(sunny_side[partition], line)
    end       = right+1
    search_list = [sunny_side[partition]]

    # Begin loop, only terminates when shortest distance is found
    while True:

        if partition == left: # length < 3, only two or less options to choose from
            
            if partition == right: # length of 1, must be smallest
                return (mid_dist, partition, sunny_side[partition], search_list)

            else: # length of 2, compare left to right
                next_vertex = sunny_side[right]
                next_dist = MyGeometry.pointLineDistance(next_vertex, line)
                search_list.append(next_vertex)

                if mid_dist <= next_dist: # left is smallest
                    return (mid_dist, partition, sunny_side[partition], search_list)

                else: # right is smallest
                    return (next_dist, right, next_vertex, search_list)

        else: # length > 2, check middle left and right
            next_vertex = sunny_side[(partition-1)%end]
            search_list.append(next_vertex)
            next_dist = MyGeometry.pointLineDistance(next_vertex, line)

            if(next_dist < mid_dist): # left is shorter, disregard everything on the right
                right     = partition-1
                partition = int((left+right)/2)
                next_vertex = sunny_side[partition]
                mid_dist  = MyGeometry.pointLineDistance(next_vertex, line)
                search_list.append(next_vertex)
            else:
                next_vertex = sunny_side[partition+1]
                next_dist   = MyGeometry.pointLineDistance(next_vertex, line)
                search_list.append(next_vertex)

                if next_dist < mid_dist: # right is shorter, disregard everything on the left
                    left = partition+1
                    partition = int((left+right)/2)
                    next_vertex = sunny_side[partition]
                    mid_dist = MyGeometry.pointLineDistance(next_vertex, line)
                    search_list.append(next_vertex)

                else: # The middle is the shortest length. 
                    return (mid_dist, partition, sunny_side[partition], search_list)



# Checks every vertex and takes the shortest distance to the line
# For benchmark purposes  
def bruteForceDistance(polygon, line):

    vertices   = polygon.getVertices()
    short_vert = vertices[0]
    index      = 0
    ldistance  = MyGeometry.pointLineDistance(short_vert, line)

    for i in range(1, len(vertices)):
        this_distance = MyGeometry.pointLineDistance(vertices[i], line)

        if this_distance < ldistance:
            ldistance  = this_distance
            index      = i
            short_vert = vertices[i]

    return (ldistance, index, short_vert)

