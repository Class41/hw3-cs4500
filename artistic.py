"""
# Vasyl Onufriyev
# CS4500 Miller
# 9.20.19

# Purpose #

This application creates works of art by dropping "paint blobs" across a given
grid size. Paintings are complete only when all squares on the aforementioned
grid are filled with at least one blob. This proccesses is repeated a specified
number of times

# Requirements #

1. On the screen, ask the interactive user to enter an integer between 2 and 15
   inclusive. This will determine the size of your square grid. I will call this
   number N. If the user enters something illegal, give an error message and
   keep asking until you get something appropriate.
2. Next, ask the interactive user to enter an integer between 1 and 10
   inclusive. This will tell your program how many “paintings” it will make. I
   will call this number K. If the user enters something illegal, give an error
   message and keep asking until you get something appropriate.
3. Make an N X N random paint blob painting K times. As each of the K paintings
   is being made, display graphics on the screen to show the interactive user
   how the painting is proceeding. You have great latitude as to how you will
   display the painting as it fills up with paint. At the very least, the
   interactive user should be able to tell which cells have NO paint so far,
   which cells have SOME paint so far, and which cell is being painted right at
   the moment. This minimum would require three distinct colors. However, you
   might be able to think of a clever way to visually communicate more
   information about the painting than no paint, some paint, and currently being
   painted. Be thoughtful and creative about this, please. Give some thought as
   to how quickly you want to paint drops to appear in your simulation.
4. After a painting “finishes,” alert the interactive user, and inform them that
   they must push ENTER (or RETURN) to continue.
5. After all K paintings have been finished (including the final ENTER push by
   the user), display the following statistics from all the paintings: The
   minimum, maximum, and average number of paint blobs it took to paint a
   picture; and the minimum, maximum, and average number that describes the most
   paint blobs that fell into any one cell in a painting. 

# Operation specific description #

When program starts, the user is asked what their grid size preference is, after
a value is entered (N) and ENTER is pressed, the user will be asked how many of
these paintings they would like the program to complete (K). After a number is
entered and ENTER is pressed, a GUI will appear and a grid of size N x N will be
drawn. If a grid cell has no paint in it, it will be highlighted with a
light-gray outline, if a cell has paint, it will have no border. If a cell is
currently being painted into, it will get a hot-pink outline which is then
removed on the next cycle. The proccess of placing ink blobs on the N x N grid
continues until the painting is complete--that is when no gray cells exist/all
cells have a paint blob. At which point, the user can admire the painting and
press ENTER or RETURN to continue onto the next artwork repeating the cycle K
many times.

"""
import turtle
import random

# Sets the width/height of the window that is drawn into WARNING: Aspect ratio
# may be wonky
SCREEN_SIZE = 500


# Handles user input of grid size (N)
def getDimensions():
    valid = False
    N = -1

    print("Please specify your grid-size")

    while (
        not valid
    ):  # valid requires number to be in requested range and be parsable to a int
        N = input("Please enter an integer between 2 and 15 inclusive: ")

        try:  # if this passes, we know N is within range and is also parsable to an int
            N = int(N)
            if N >= 2 and N <= 15:  # bounds for input
                valid = True
            else:
                print("That is not in the allowed range. Try again.")

        except Exception as err:
            print("That's not a number. Try again.")

    return N


# Handles user input of painting count (K)
def getNumPaintings():
    valid = False
    N = -1

    print("Select a number of paintings to be completed by ze artist")

    while (
        not valid
    ):  # valid requires number to be in requested range and be parsable to a int
        N = input("Please enter an integer between 1 and 10 inclusive: ")

        try:  # if this passes, we know N is within range and is also parsable to an int
            N = int(N)
            if N >= 1 and N <= 10:  # bounds for input
                valid = True
            else:
                print("That is not in the allowed range. Try again.")

        except Exception as err:
            print("That's not a number. Try again.")

    return N


# Setup the screen size/speed for the turtle, reset origin, and returns the
# turtle
def setupTurtle():
    turtle.setup(SCREEN_SIZE, SCREEN_SIZE)  # setup play area
    turtle.setworldcoordinates(
        0, SCREEN_SIZE + 10, SCREEN_SIZE + 10, 0
    )  # reset origin for turtle
    screen = turtle.Screen()  # create new screen instance
    screen.delay(0)  # don't spend time drawing, it takes too long!
    screen.reset()
    screen.bgcolor("black")

    return turtle.Turtle()


# Draws a grid of N x N in color color using turtle turt
def drawGrid(turt, N, color):
    turt.speed("fast")
    turt.color(color)

    gridlineIncrement = SCREEN_SIZE / N  # Calculates spacing between gridlines

    # This section draws the outer outline of the grid
    turt.goto(SCREEN_SIZE, 0)
    turt.goto(SCREEN_SIZE, SCREEN_SIZE)
    turt.goto(0, SCREEN_SIZE)
    turt.goto(0, 0)

    # Efficiently draw vertical lines, alternating up/down to minimize travel
    # time
    for i in range(1, N):
        turt.penup()
        if i % 2 == 1:
            turt.goto(gridlineIncrement * i, 0)
            turt.pendown()
            turt.goto(gridlineIncrement * i, SCREEN_SIZE)
        else:
            turt.goto(gridlineIncrement * i, SCREEN_SIZE)
            turt.pendown()
            turt.goto(gridlineIncrement * i, 0)

    # Efficiently draw horizontal lines, alternating left/right to minimize
    # travel time
    for i in range(1, N):
        turt.penup()
        if i % 2 == 1:
            turt.goto(0, gridlineIncrement * i)
            turt.pendown()
            turt.goto(SCREEN_SIZE, gridlineIncrement * i)
        else:
            turt.goto(SCREEN_SIZE, gridlineIncrement * i)
            turt.pendown()
            turt.goto(0, gridlineIncrement * i)

    # Return turtle to origin
    turt.penup()
    turt.goto(0, 0)
    turt.pendown()
    turt.speed("normal")


# Calculates and goes to a grid cell center
def gotoGridCoordCenter(turt, N, xcoord, ycoord):
    gridlineIncrement = SCREEN_SIZE / N
    turt.penup()
    turt.goto(
        (gridlineIncrement * xcoord) - (gridlineIncrement / 2),
        (gridlineIncrement * ycoord) - (gridlineIncrement / 2),
    )
    turt.pendown()


# Calculates the bounding box of a grid cell and returns a list of mins/maxes
def getGridCoordConstraints(turt, N, xcoord, ycoord):
    gridlineIncrement = SCREEN_SIZE / N
    xcenter = (gridlineIncrement * xcoord) - (
        gridlineIncrement / 2
    )  # Calculate center x
    ycenter = (gridlineIncrement * ycoord) - (
        gridlineIncrement / 2
    )  # Calculate center y

    # Starting at the center, add a 1/2 increment of the gridline in each
    # direction
    xmin = int(xcenter - (gridlineIncrement / 2))
    xmax = int(xcenter + (gridlineIncrement / 2))
    ymin = int(ycenter - (gridlineIncrement / 2))
    ymax = int(ycenter + (gridlineIncrement / 2))

    return [xmin, xmax, ymin, ymax]


# Outlines a cell at xcoord ycoord in color color using turtle turt
def higlightGridSquare(turt, N, xcoord, ycoord, color):
    gridlineIncrement = SCREEN_SIZE / N

    originalColor = turt.color()  # Save incoming turtle color

    turt.color(color)
    turt.penup()
    turt.goto(
        gridlineIncrement * xcoord, gridlineIncrement * ycoord
    )  # Goes to top left corner of cell outline
    turt.pendown()

    # This section traces around the grid cell
    turt.goto(
        (gridlineIncrement * xcoord) + gridlineIncrement, gridlineIncrement * ycoord
    )
    turt.goto(
        (gridlineIncrement * xcoord) + gridlineIncrement,
        (gridlineIncrement * ycoord) + gridlineIncrement,
    )
    turt.goto(
        gridlineIncrement * xcoord, (gridlineIncrement * ycoord) + gridlineIncrement
    )
    turt.goto(gridlineIncrement * xcoord, gridlineIncrement * ycoord)

    turt.color(originalColor[0])  # Return the turtle back to the color it came in as


# Loops through the 2D array containing colored/uncolored flags and colors or
# re-draws cell outlines as needed depending on the painstates 2D array. This is
# required due to redrawing the entire grid takes too long! This is for
# efficiency. We only redraw potentially affected cells
def colorizeCoverage(turt, N, matrix, paintstates, colorset):
    for i in range(0, N):
        for j in range(0, N):
            if (
                matrix[i][j] == 1 and paintstates[i][j] == 2
            ):  # Executes if cell is flagged for redraw, and the cell is filled with blob(s)
                paintstates[i][j] = 1
            if (
                matrix[i][j] == 0 and paintstates[i][j] == 2
            ):  # Executes if flagged and unpainted cell
                higlightGridSquare(turt, N, i, j, colorset["unpainted"])
                paintstates[i][j] = 0


# Checks the current grid state to make sure all cells have at least one blob
def verifyCoverage(matrix, N):
    for i in range(0, N):
        for j in range(0, N):
            if matrix[i][j] == 0:
                return (
                    False
                )  # If there is at least one that has zero blobs, we don't care about the rest
    return True


# For efficiency reasons, flags a + pattern around the updated cell at xcoord
# ycoord for redraw
def updateMatrixCross(N, paintstates, xcoord, ycoord):
    paintstates[xcoord][ycoord] = 1  # Flag self as painted

    if xcoord + 1 < N:  # Right of +
        paintstates[xcoord + 1][ycoord] = 2
    if ycoord + 1 < N:  # Top of +
        paintstates[xcoord][ycoord + 1] = 2
    if xcoord - 1 >= 0:  # Left of +
        paintstates[xcoord - 1][ycoord] = 2
    if ycoord - 1 >= 0:  # Bottom of +
        paintstates[xcoord][ycoord - 1] = 2

    return paintstates


# Handles keeping track of painted cells, and issuing paint calls to cells from
# random number generation
def createArt(turt, N, colorset):
    # 2D arrays
    colored = [
        [0 for x in range(N)] for y in range(N)
    ]  # Stores 1 or 0 if cell painted or unpainted respectively
    paintstates = [
        [0 for x in range(N)] for y in range(N)
    ]  # Used for algorithm optimization
    coloredcount = [
        [0 for x in range(N)] for y in range(N)
    ]  # Stores statistical data for artwork

    while (
        verifyCoverage(colored, N) == False
    ):  # While we still have cells that are unpainted
        
        # Select a random cell from the grid
        k = random.randint(1, N)
        j = random.randint(1, N)

        colorizeCoverage(
            turt, N, colored, paintstates, colorset
        )  # Repaint the grid masked to flagged cells
        higlightGridSquare(
            turt, N, k - 1, j - 1, colorset["painting"]
        )  # Highlight the square we are about to paint
        paintstates = updateMatrixCross(N, paintstates, k - 1, j - 1)  # Set flags for +

        constraints = getGridCoordConstraints(
            turt, N, k, j
        )  # Get grid cell bounding box

        turt.speed("fastest")  # GO HYPERDRIVE
        turt.ht()  # The user doesn't need to see this madness, and also speeds up the drawing

        radius = int(
            SCREEN_SIZE / (N * random.randint(4, 25))
        )  # Generate random blob radius

        # Select a random coord within the boundingbox of the selected cell
        xcord = random.randint(
            int(constraints[0]) + radius + 5, int(constraints[1]) - radius - 5
        )
        ycord = random.randint(
            int(constraints[2]) + 5, int(constraints[3]) - (2 * radius) - 5
        )

        turt.color(
            list(colorset.values())[3 + random.randint(0, 2)]
        )  # Select random color from the colorset

        # This section goes to the selected coord and draws a filled circle of
        # radius radius in color selected above
        turt.penup()
        turt.goto(xcord, ycord)
        turt.pendown()
        turt.begin_fill()
        turt.circle(radius)
        turt.end_fill()

        # Update 2D arrays
        colored[k - 1][j - 1] = 1  # Flag this cell as colored
        coloredcount[k - 1][j - 1] = (
            coloredcount[k - 1][j - 1] + 1
        )  # Update statistics 2D array
        higlightGridSquare(
            turt, N, k - 1, j - 1, colorset["painted"]
        )  # Remove outline on current cell

    colorizeCoverage(
        turt, N, colored, paintstates, colorset
    )  # After art finishes, redraw the grid one last time
    return coloredcount


# Modify overall statistics based on the results of the last piece of art
def gatherArtStatistics(resultset, results, N):
    cell_min = 99999
    cell_max = 0
    art_total = 0

    # print(str(results).replace("],", "]\n", -1))

    # Loop through the results from last art (blob counts)
    for i in range(0, N):
        for j in range(0, N):
            art_total = art_total + results[i][j]

            if results[i][j] < cell_min:
                cell_min = results[i][j]
            if results[i][j] > cell_max:
                cell_max = results[i][j]

    resultset["art_avg"] = resultset["art_avg"] + art_total

    # Update overall art statistics
    if resultset["art_min"] > art_total:
        resultset["art_min"] = art_total
    if resultset["art_max"] < art_total:
        resultset["art_max"] = art_total

    resultset["cell_avg"] = resultset["cell_avg"] + art_total

    # Update overall cell statistics
    if resultset["cell_min"] > cell_min:
        resultset["cell_min"] = cell_min
    if resultset["cell_max"] < cell_max:
        resultset["cell_max"] = cell_max

    return resultset


# Performs average divisions and displays the resultset to the screen
def finalizeAndDisplayResults(resultset, N, numpaintings):
    resultset["cell_avg"] = resultset["cell_avg"] / (
        N * N * numpaintings
    )  # N*N Cells Numpaintings times
    resultset["art_avg"] = resultset["art_avg"] / numpaintings  # Paintings blob average

    # Print results to screen
    print("Min blobs to complete a piece of art: " + str(resultset["art_min"]))
    print("Max blobs to complete a piece of art: " + str(resultset["art_max"]))
    print("Avg blobs to complete a piece of art: " + str(resultset["art_avg"]))
    print("\n\nMin blobs in a cell: " + str(resultset["cell_min"]))
    print("Max blobs in a cell: " + str(resultset["cell_max"]))
    print("Avg blobs in a cell: " + str(resultset["cell_avg"]))


# Program entrypoint
def startApp():

    colorset = {  # Colors that are used for cell outlines and blob colors
        "unpainted": "#404040",
        "painted": "black",
        "painting": "#ff00bf",
        "color1": "#ff5252",
        "color2": "#ff793f",
        "color3": "#ffb142",
    }

    resultset = {  # Contains the statistics data displayed at the end of loops
        "art_min": 99999,
        "art_max": 0,
        "art_avg": 0,
        "cell_min": 99999,
        "cell_max": 0,
        "cell_avg": 0,
    }

    # Gets user inputs
    N = getDimensions()
    numPaintings = getNumPaintings()

    # Loops for each painting
    for i in range(0, numPaintings):
        turt = setupTurtle()  # Recreate the canvas
        drawGrid(turt, N, colorset["unpainted"])  # Recreate the grid

        results = createArt(turt, N, colorset)  # Create art and capture staistics
        resultset = gatherArtStatistics(resultset, results, N)  # Update result set
        input("Push ENTER or RETURN to continue...")  # Await user input

    finalizeAndDisplayResults(
        resultset, N, numPaintings
    )  # After all paintings, display statistics


# Capture entrypoint call
if __name__ == "__main__":
    startApp()
