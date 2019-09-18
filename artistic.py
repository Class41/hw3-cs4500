import turtle

SCREEN_SIZE = 750


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
    turtle.setworldcoordinates(0, 760, 760, 0)
    screen = turtle.Screen()
    screen.register_shape("blob.gif")

    return turtle.Turtle()
    # t.shape("blob.gif")
    # screen.mainloop()


def drawGrid(turt, N):
    turt.speed("fast")
    
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
    turt.goto(0,0)
    turt.pendown()
    turt.speed("normal")


def startApp():
    N = getDimensions()
    numPaintings = getNumPaintings()
    turt = setupTurtle()
    drawGrid(turt, N)
    input()


if __name__ == "__main__":
    startApp()
