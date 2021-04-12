# PolygonDistance

* [About](#about)
* [How to Use](#how-to-use)
* [Project Structure](#project-structure)
* [Pseudocode](#pseudocode)

---

## About

This is an educational application, which can generate random convex polygons, measure the shortest distance between a given convex polygon and a given line, and create diagrams of the results.

## How to Use

In the terminal or windows command prompt navigate to the base directory and enter `python src/main.py`. This will bring up the gui.

 The `Generate Polygon` button will create a screen where random polygons can be generated and saved to file. Note that if you wish to use this file with the diagram generator, a line equation in the form `ax+by=c` must be manually appnded to the bottom of the text file. Format is not strict, as long as the line equation comes after the list of vertices and the parameters are separated by some non-digit separator, the file should be accepted by the diagram generator.

 The `Load File` button will bring up a load file dialog. Select a file with the below specified input file format and then a solution to find the shortest distance between the given line and polygon will be generated. You can then choose to save the result, or just view it in a temporary file.

 ### File Format

 The file format is as follows: 
 * an integer specifying the number (n) of vertices in the polygon
 * 2*n integers denoting (x,y) pairs of coordinates for the vertices of the polygon is counter-clockwise order.
 * three integers specifying the a, b, and c of the line equation ax+by=c

 Order matters but format is otherwise not strict.

 ## Project Structure

 In the `Examples` directory, several pre-generated exmaple input and output files are included.

 Source code is all within the `src` directory, with the following files:

 ## [`main`](./src/main.py)

 Simple entry point for the GUI and program.

 ## [`MyPolygon`](./src/MyPolygon.py)

 A small file containing simple objects for polygons and lines. Made early in development and a bit redundant. 

 ## [`MyGeometry`](./src/MyGeometry.py)

 Contains several algorithms for computing geometrical equations. 

 ## [`MyCollision`](./src/MyCollision.py)

 File that contains the main algorithms for computing the distance between a polygon and a line. Contains both a 'brute force' algorithm, and an algorithm that incorporates binary search.

 ## [`GeneratePolygon`](./src/GeneratePolygon.py)

 Contains the algorithm used to generate random polygons with a specified number of vertices contained in a specified region, as well as a function for printing the polygon to file.

 Most if not all of the work in the random polygon generator is not mine, but taken from [https://cglab.ca/~sander/misc/ConvexGeneration/convex.html](https://cglab.ca/~sander/misc/ConvexGeneration/convex.html).

 ## [`ReadFile`](./src/ReadFile.py)

 Contains the algorithm used to parse the input files and produces a set of vertices as a list of 2-tuples and a line as a 3-tuple.

 ## [`DrawDiagram`](./src/DrawDiagram.py)

 Contains all the logic used for generating the diagrams based on solutions given. 

 ## [`PolygonGUI`](./src/PolygonGUI.py)

 Contains all logic used for the gui. 

 ## Test Files

 I've decided to retain some test files that were used during development. They are all named by the convention `test_.py` and serve no function to the completed project, but demonstrate some of the various functions of my project.

 # Pseudocode

 Included below is pseudocode for the algorithm that uses binary search in order to find the shortest distance between a polygon and a line:

 ````
 find sunny side:
    input = polygon

    find center of polygon's vertices

    take the projection of the center on the line
    and then derive the directional vector

    for the directional vector:

        if magnitude of x is greater than 
        the magnitude of y:

            if x is positive:
                return the right half of vertices
            else x is negative:
                return the left half of vertices

        else magnitude of y is greater:
            
            if y is positive:
                return the top half of vertices
            else y is negative:
                return the bottom half of vertices

binary seach for distance:
    input = sunny side

    let left be the first vertex in sunny side
    let right be the last vertex in sunny side
    let middle be the middle most vertex

    loop until closest vertex is found:

        if distance to line from middle-1 is less
        than the distance to line from middle:

            let right be middle-1
            let middle be vertex halfway between
            left and right

        else if distance to line from middle+1 is 
        less than the distance to line from middle:

            let left be middle+1
            let middle be vertex halfway between
            left and right

        otherwise:

            middle is the closest vertex
            return middle 

 ````