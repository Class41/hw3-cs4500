import turtle

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
    screen = turtle.Screen()
    screen.register_shape("blob.gif")


    t = turtle.Turtle()
    t.turtlesize(50, 50, None)
    t.shape("blob.gif")

    #screen.mainloop()

def startApp():
    setupTurtle()
    getDimensions()
    getNumPaintings()


if __name__ == "__main__":
    startApp()
