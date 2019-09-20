import turtle
import random

SCREEN_SIZE = 500

def getDimensions():
    valid = False
    N = -1

    print("Please specify your grid-size")

    while not valid:
        N = input("Please enter an integer between 2 and 15 inclusive: ")

        try:
            N = int(N)
            if N >= 2 and N <= 15:
                valid = True
            else:
                print("That is not in the allowed range. Try again.")

        except Exception as err:
            print("That's not a number. Try again.")

    return N


def getNumPaintings():
    valid = False
    N = -1

    print("Select a number of paintings to be completed by ze artist")

    while not valid:
        N = input("Please enter an integer between 1 and 10 inclusive: ")

        try:
            N = int(N)
            if N >= 1 and N <= 10:
                valid = True
            else:
                print("That is not in the allowed range. Try again.")

        except Exception as err:
            print("That's not a number. Try again.")

    return N


def setupTurtle():
    turtle.setup(SCREEN_SIZE, SCREEN_SIZE)
    turtle.setworldcoordinates(0, SCREEN_SIZE + 10, SCREEN_SIZE + 10, 0)
    screen = turtle.Screen()
    screen.delay(0)
    screen.reset()
    screen.bgcolor("black")

    return turtle.Turtle()


def drawGrid(turt, N, color):
    turt.speed("fast")
    turt.color(color)

    gridlineIncrement = SCREEN_SIZE / N
    turt.goto(SCREEN_SIZE, 0)
    turt.goto(SCREEN_SIZE, SCREEN_SIZE)
    turt.goto(0, SCREEN_SIZE)
    turt.goto(0, 0)

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

    turt.penup()
    turt.goto(0, 0)
    turt.pendown()
    turt.speed("normal")


def gotoGridCoordCenter(turt, N, xcoord, ycoord):
    gridlineIncrement = SCREEN_SIZE / N
    turt.penup()
    turt.goto(
        (gridlineIncrement * xcoord) - (gridlineIncrement / 2),
        (gridlineIncrement * ycoord) - (gridlineIncrement / 2),
    )
    turt.pendown()


def getGridCoordConstraints(turt, N, xcoord, ycoord):
    gridlineIncrement = SCREEN_SIZE / N
    xcenter = (gridlineIncrement * xcoord) - (gridlineIncrement / 2)
    ycenter = (gridlineIncrement * ycoord) - (gridlineIncrement / 2)

    xmin = int(xcenter - (gridlineIncrement / 2))
    xmax = int(xcenter + (gridlineIncrement / 2))
    ymin = int(ycenter - (gridlineIncrement / 2))
    ymax = int(ycenter + (gridlineIncrement / 2))

    return [xmin, xmax, ymin, ymax]

def higlightGridSquare(turt, N, xcoord, ycoord, color):
    gridlineIncrement = SCREEN_SIZE / N
    
    originalColor = turt.color()
    
    turt.color(color)
    turt.penup()
    turt.goto(gridlineIncrement * xcoord, gridlineIncrement * ycoord)
    turt.pendown()
    
    turt.goto((gridlineIncrement * xcoord) + gridlineIncrement, gridlineIncrement * ycoord)
    turt.goto((gridlineIncrement * xcoord) + gridlineIncrement, (gridlineIncrement * ycoord) + gridlineIncrement)
    turt.goto(gridlineIncrement * xcoord, (gridlineIncrement * ycoord) + gridlineIncrement)
    turt.goto(gridlineIncrement * xcoord, gridlineIncrement * ycoord)

    turt.color(originalColor[0])

def colorizeCoverage(turt, N, matrix, paintstates, colorset):                                    
    for i in range(0, N):
        for j in range (0, N):
            if matrix[i][j] == 1 and paintstates[i][j] == 2:
                paintstates[i][j] = 1
            if matrix[i][j] == 0 and paintstates[i][j] == 2:
                higlightGridSquare(turt, N, i, j, colorset["unpainted"])
                paintstates[i][j] = 0
    
def verifyCoverage(matrix, N):
    for i in range(0, N):
        for j in range (0, N):
            if matrix[i][j] == 0:
                return False
    return True

def updateMatrixCross(N, paintstates, xcoord, ycoord):
    paintstates[xcoord][ycoord] = 1
    
    if xcoord + 1 < N:
        paintstates[xcoord + 1][ycoord] = 2
    if ycoord + 1 < N:
        paintstates[xcoord][ycoord + 1] = 2
    if xcoord - 1 >= 0:
        paintstates[xcoord - 1][ycoord] = 2
    if ycoord - 1 >= 0:
        paintstates[xcoord][ycoord - 1] = 2
        
    return paintstates

def createArt(turt, N, colorset):
    colored = [[0 for x in range(N)] for y in range(N)]
    paintstates = [[0 for x in range(N)] for y in range(N)]
    coloredcount = [[0 for x in range(N)] for y in range(N)]
    
    while verifyCoverage(colored, N) == False:
        k = random.randint(1, N)
        j = random.randint(1, N)
        
        colorizeCoverage(turt, N, colored, paintstates, colorset)
        higlightGridSquare(turt, N, k - 1, j - 1, colorset["painting"])
        paintstates = updateMatrixCross(N, paintstates, k - 1, j - 1)        

        constraints = getGridCoordConstraints(turt, N, k, j)
        
        turt.speed("fastest")
        turt.ht()
        
        radius = int(SCREEN_SIZE / (N* random.randint(4,12)))
        
        xcord = random.randint(int(constraints[0]) + radius + 5, int(constraints[1]) - radius - 5)
        ycord = random.randint(int(constraints[2]) + 5, int(constraints[3]) - (2*radius) - 5)
        
        turt.color(list(colorset.values())[3 + random.randint(0, 2)])
        
        turt.penup()
        turt.goto(xcord, ycord)
        turt.pendown()
        turt.begin_fill()
        turt.circle(radius)
        turt.end_fill()
        colored[k - 1][j - 1] = 1
        coloredcount[k - 1][j - 1] = coloredcount[k - 1][j - 1] + 1
        higlightGridSquare(turt, N, k - 1, j - 1, colorset["painted"])
    
    colorizeCoverage(turt, N, colored, paintstates, colorset)
    return coloredcount

def gatherArtStatistics(resultset, results, N):
    cell_min = 99999
    cell_max = 0
    art_total = 0
    
    #print(str(results).replace("],", "]\n", -1))
    
    for i in range(0, N):
        for j in range (0, N):
            art_total = art_total + results[i][j]
            
            if results[i][j] < cell_min:
                cell_min = results[i][j]
            if results[i][j] > cell_max:
                cell_max = results[i][j]
        
    resultset["art_avg"] = resultset["art_avg"] + art_total
    
    if resultset["art_min"] > art_total:
        resultset["art_min"] = art_total
    if resultset["art_max"] < art_total:
        resultset["art_max"] = art_total
    
    resultset["cell_avg"] = resultset["cell_avg"] + art_total
    
    if resultset["cell_min"] > cell_min:
        resultset["cell_min"] = cell_min
    if resultset["cell_max"] < cell_max:
        resultset["cell_max"] = cell_max
        
    return resultset

def finalizeAndDisplayResults(resultset, N, numpaintings):
    resultset["cell_avg"] = resultset["cell_avg"] / (N*N*numpaintings)
    resultset["art_avg"] = resultset["art_avg"] / numpaintings
    
    print("Min blobs to complete a piece of art: " + str(resultset["art_min"]))
    print("Max blobs to complete a piece of art: " + str(resultset["art_max"]))
    print("Avg blobs to complete a piece of art: " + str(resultset["art_avg"]))
    print("\n\nMin blobs in a cell: " + str(resultset["cell_min"]))
    print("Max blobs in a cell: " + str(resultset["cell_max"]))
    print("Avg blobs in a cell: " + str(resultset["cell_avg"]))

    
def startApp():
    
    colorset = {
        "unpainted":"#404040",
        "painted":"black",
        "painting":"#ff00bf",
        "color1":"#ff5252",
        "color2":"#ff793f",
        "color3":"#ffb142"
    }
    
    resultset = {
        "art_min":99999,
        "art_max": 0,
        "art_avg": 0,
        "cell_min": 99999,
        "cell_max": 0,
        "cell_avg": 0
    }
    
    N = getDimensions()
    numPaintings = getNumPaintings()
    
    for i in range(0, numPaintings):
        turt = setupTurtle()
        drawGrid(turt, N, colorset["unpainted"])
        results = createArt(turt, N, colorset)
        resultset = gatherArtStatistics(resultset, results, N)
        input()
    
    finalizeAndDisplayResults(resultset, N, numPaintings)


if __name__ == "__main__":
    startApp()
