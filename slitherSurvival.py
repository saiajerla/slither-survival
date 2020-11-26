import pygame 
import random,time

WIDTH = 500
HEIGHT = 500

def main():
    #create a screen
    pygame.display.init()
    clock = pygame.time.Clock()

    #creating a window
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Slither Survival")

    #displaying instructions
    introMessage(window)
    
    snakeWidth = 10
    foodWidth = 10
    
    #Getting a random location for the snake to start at
    snakex = WIDTH // 2
    snakey = HEIGHT // 2

    #Getting a random location for the placement of food
    foodx, foody = foodLocations(snakex,snakey)

    xDirection = 0
    yDirection = 0

    snakeLength = 0

    #a list to keep track of all positions visited
    slist = []
    
    while True:
        window.fill((0,0,0))
        
        #getting the indices depending on the key pressed
        xDirection, yDirection = handlingEvents(xDirection, yDirection)

        #moving the snake 
        snakex = snakex + xDirection
        snakey = snakey + yDirection
        slist.append([snakex,snakey])

        #Exiting the game if the snake touches the boundaries
        if (snakex <= 0 or snakex >= WIDTH) or (snakey <= 0 or snakey >= HEIGHT):
            exitMessage(window,snakeLength)
            pygame.display.update()
            time.sleep(2)
            break
        
        #If the length of the snake is more than 1,
        #getting the positions required for the length of snake
        if snakeLength > 0:
            val = bodySnake(snakeLength,slist,window)
            if val == 0:
                exitMessage(window,snakeLength)
                pygame.display.update()
                time.sleep(2)
                break
        else:
            pygame.draw.rect(window, (0, 255, 0), [snakex, snakey, snakeWidth, snakeWidth])

        #drawing the food icon
        pygame.draw.circle(window, (255,0,0), (foodx,foody), foodWidth/2)

        #getting new location of food if the snake ate food
        if (foodx-foodWidth <= snakex <= foodx+foodWidth and foody-foodWidth <= snakey <= foody+foodWidth):
             foodx, foody = foodLocations(snakex,snakey)
             snakeLength = snakeLength + 1

        #displaying the score of the game
        score(window,snakeLength)
        pygame.display.update()

        clock.tick(15)
    pygame.quit()
    quit()

def foodLocations(snakex,snakey):
    foodWidth = 10
    foodx = random.randint(foodWidth*(foodWidth//2), WIDTH - foodWidth*(foodWidth//2))
    foody = random.randint(foodWidth*(foodWidth//2), HEIGHT - foodWidth*(foodWidth//2))
    return foodx,foody

def handlingEvents(xDirection, yDirection):
    snakeWidth = 10
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            break 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xDirection = -1 * snakeWidth
                yDirection = 0
            elif event.key ==  pygame.K_RIGHT:
                xDirection = snakeWidth
                yDirection = 0
            elif event.key == pygame.K_UP:
                yDirection = -1 * snakeWidth
                xDirection = 0
            elif event.key == pygame.K_DOWN:
                yDirection = snakeWidth
                xDirection = 0
            elif event.key == pygame.K_RETURN:
                return "continue"
            elif event.key == pygame.K_ESCAPE:
                exit()

    return xDirection, yDirection
                
def exitMessage(window, value):
    pygame.font.init()
    fontObj = pygame.font.SysFont("", 40) #displaying the exit messages
    
    text1 = fontObj.render("GAME OVER!", True, (255, 255, 255))
    text2 = fontObj.render("Final score: "+str(value), True, (255, 255, 255))
    text3 = fontObj.render("Thanks for playing!", True, (255, 255, 255))
    
    window.blit(text1,(WIDTH//4,HEIGHT//4))
    window.blit(text2,(WIDTH//4,HEIGHT//3))
    window.blit(text3,(WIDTH//4,HEIGHT//2))
            
def snake(sbody, window):
    snakeWidth = 10
    for i in sbody: #displaying the body of the snake
        pygame.draw.rect(window, (0, 255, 0), [i[0], i[1], snakeWidth, snakeWidth])

def score(window,value):
    pygame.font.init() #displaying the score on top left corner 
    fontObj = pygame.font.SysFont("Score: ", 40) #updating score values each time
    text = fontObj.render("Score: " + str(value), True, (255, 255, 255))

    window.blit(text,(10,10))

def bodySnake(snakeLength,slist,window):
    #getting the locations of the body of the snake
    snakeLocations = [] 
    counter = 0

    #getting only the body of the snake
    for i in reversed(slist):
        if snakeLength+1 == counter:
            break
        else:
            snakeLocations.append(i)
            counter = counter + 1

    #checking if snake is biting itself       
    head = snakeLocations[0]
        
    if head in snakeLocations[1:]:
        return 0
        
    snake(snakeLocations,window) #drawing the snake

def introMessage(window):
    pygame.font.init()
    fontObj = pygame.font.SysFont("", 30)
    fontObj2 = pygame.font.SysFont("", 20)

    textMain = ["Welcome to the Slither Survival Game!", "Instructions:"]
    textSub = ["Use the 4 arrows on your keyboard to move the snake.", "You can score points by eating the food items.", "When the snake eats an item, it gets longer.", "The game ends if the snake hits the borders or runs into it's own body.", "The final score depends on the total number of food items eaten by the snake.","Press 'ENTER' to start the game.","Press 'ESC' to exit the game."]

    x1 = 10
    y1 = 20

    #displaying the main heading instructions on the window
    for i in textMain:
        text = fontObj.render(i, True, (255, 0, 0))
        window.blit(text, (x1,y1))
        y1 = y1+40

    #displaying the sub heading instructions on the window
    for j in textSub:
        text = fontObj2.render(j, True, (255, 255, 255))
        window.blit(text, (x1,y1))
        y1 = y1+20

    #displaying the image on the window
    picture = pygame.image.load("goodLuck.png")
    window.blit(pygame.transform.scale(picture, (200, 200)), (WIDTH//2,HEIGHT//2))
    pygame.display.update()
    
    while True:
        entered = handlingEvents(0,0)
        if entered == "continue":
            break
    
main()
