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
    screen.register_shape("blob.gif")
    screen.delay(0)
    screen.bgcolor("black")

    return turtle.Turtle()
    # t.shape("blob.gif")
    # screen.mainloop()


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
    
    turt.goto((2 * gridlineIncrement) * xcoord, gridlineIncrement * ycoord)
    turt.goto((2 * gridlineIncrement) * xcoord, (2 * gridlineIncrement) * ycoord)
    turt.goto(gridlineIncrement * xcoord, (2 * gridlineIncrement) * ycoord)
    turt.goto(gridlineIncrement * xcoord, gridlineIncrement * ycoord)

    turt.color(originalColor[0])

def verifyCoverage(matrix, N):
    for i in range(0, N):
        for j in range (0, N):
            if matrix[i][j] == 0:
                return False
    return True

def createArt(turt, N, colorset):
    colored = [[0 for x in range(N)] for y in range(N)]
    coloredCount = [[0 for x in range(N)] for y in range(N)]
    
    while verifyCoverage(colored, N) == False:
        k = random.randint(1, N)
        j = random.randint(1, N)
        
        constraints = getGridCoordConstraints(turt, N, k, j)
        
        turt.speed("fastest")
        turt.ht()
        
        radius = int(SCREEN_SIZE / (N*5))
        
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
        coloredCount[k - 1][j - 1] = coloredCount[k - 1][j - 1] + 1

def startApp():
    
    colorset = {
        "unpainted":"#404040",
        "painted":"#8c8c8c",
        "painting":"#ff00bf",
        "color1":"#ff5252",
        "color2":"#ff793f",
        "color3":"#ffb142"
    }
    
    N = getDimensions()
    numPaintings = getNumPaintings()
    turt = setupTurtle()
    drawGrid(turt, N, colorset["unpainted"])
    createArt(turt, N, colorset)

    input()


if __name__ == "__main__":
    startApp()
