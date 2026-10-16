import pygame
import random

pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(400,50)

screenWidth = 1280
screenHeight = 720
window = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
screen = pygame.Surface((screenWidth, screenHeight))

menuBackground = pygame.image.load("menu.jpeg")
menuBackground = pygame.transform.scale(menuBackground, (screenWidth, screenHeight))
gameBackground = pygame.image.load("game.jpeg")
gameBackground = pygame.transform.scale(gameBackground, (screenWidth, screenHeight))

running = True
active = False

gameState = "menu"
highestScore = 0
score = 0

titleFont = pygame.font.Font(None, 100)
font = pygame.font.Font(None, 50)

words = ["CLOUD", "TEMPERATURE", "RAIN", 
         "STARS", "NIMBUS", "SKY", 
         "NIGHT", "INCONSPICUOUS", "SCENIC", 
         "ATMOSPHERE", "NIMBUS", "ALTITUDE", 
         "STRATOSPHERE", "NOSTALGIA", "HAIL", 
         "WINDY", "COLD"]

speed = 5
wordSpawnTime = 2000 # This is in milliseconds, so 2000ms = 2 seconds
lastWordSpawn = 0
wordsOnScreen = []

# Menu Setup
playButton = pygame.Rect((screenWidth - 200) // 2, (screenHeight - 50) // 2, 200, 50)

def resizeWindow(event):
     global window

     window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)


def convertToGamePosition(pos):
     windowWidth = window.get_size()[0]
     windowHeight = window.get_size()[1]

     gameX = int(pos[0] * screenWidth / windowWidth)
     gameY = int(pos[1] * screenHeight / windowHeight)

     return gameX, gameY
def drawMenu(screen, titleFont, font, playButton):

    screen.blit(menuBackground, (0, 0))

    titleText = titleFont.render("TypeFast", True, "white")
    titleRect = titleText.get_rect(center=(screenWidth // 2, int(screenHeight * 0.28)))
    screen.blit(titleText, titleRect)

    if playButton.collidepoint(convertToGamePosition(pygame.mouse.get_pos())):
        buttonColor = "white"
    else:
        buttonColor = "skyblue"

    pygame.draw.rect(screen, buttonColor, playButton, border_radius = 10)

    playText = font.render("Play", True, "black")
    playTextRect = playText.get_rect(center=playButton.center)
    screen.blit(playText, playTextRect)

# Game Over Setup
tryAgainButton = pygame.Rect((screenWidth - 200) // 2, (screenHeight - 50) // 2, 200, 50)

returnButton = pygame.Rect((screenWidth - 200) // 2, (screenHeight - 50) // 2 + 100, 200, 50)

def drawGameOver(screen, titleFont, font, tryAgainButton, returnButton, wordsOnScreen):

    drawWords(screen, wordsOnScreen, font)

    gameOverText = titleFont.render("Game Over", True, "white")
    gameOverRect = gameOverText.get_rect(center=(screenWidth // 2, int(screenHeight * 0.28)))
    screen.blit(gameOverText, gameOverRect)

    if tryAgainButton.collidepoint(convertToGamePosition(pygame.mouse.get_pos())):
            tryAgainColor = "white"
    else:
        tryAgainColor = "skyblue"

    pygame.draw.rect(screen, tryAgainColor, tryAgainButton, border_radius = 10)
    tryAgainText = font.render("Try Again", True, "black")
    tryAgainTextRect = tryAgainText.get_rect(center=tryAgainButton.center)
    screen.blit(tryAgainText, tryAgainTextRect)

    if returnButton.collidepoint(convertToGamePosition(pygame.mouse.get_pos())):
            returnColor = "white"
    else:
        returnColor = "skyblue"

    pygame.draw.rect(screen, returnColor, returnButton, border_radius = 10)
    returnTextFont = pygame.font.Font(None, 35)
    returnText = returnTextFont.render("Return to menu", True, "black")
    returnTextRect = returnText.get_rect(center=returnButton.center)
    screen.blit(returnText, returnTextRect)

def drawScore(screen, font, score):
    scoreText = font.render("Score: " + str(score), True, "white")
    scoreRect = scoreText.get_rect(topleft = (int(20 * (screenWidth / 1280)), 20))
    screen.blit(scoreText, scoreRect)

def eventHandler(wordsOnScreen, textbox, userText, active, score):
    
    running = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            resizeWindow(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if textbox.collidepoint(convertToGamePosition(event.pos)):
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_BACKSPACE:
                userText = userText[:-1]
            # Checks if the user typed the correct word
            elif event.key == pygame.K_RETURN:
                for word in wordsOnScreen:
                    if word["text"] == userText and word["color"] == "gray":
                        word["color"] = "white"
                        score += 1
                        break
                userText = ""
            else:
                userText += event.unicode.upper()
    return running, userText, active, score
    

# User textbox Setup
textboxWidth = (screenWidth - 600) // 2
textboxHeight = screenHeight - 80
textbox = pygame.Rect(textboxWidth,textboxHeight, 600, 50)
textboxFont = pygame.font.Font(None, 30)
userText = ""
placeholderText = "Type fast before the word reaches the end!"

def drawtextbox(screen, textbox, userText, active, placeholderText):

    pygame.draw.rect(screen, "white", textbox, 2, border_radius = 10)
    if userText == "" and not active:
        boxText = textboxFont.render(placeholderText, True, "grey")
    else:
        boxText = textboxFont.render(userText, True, "white")

    boxTextRect = boxText.get_rect(midleft=(textbox.x + 10, textbox.centery))
    screen.blit(boxText, boxTextRect)

def spawnWord(words, wordsOnScreen):

    newWord = random.choice(words)
    wordsOnScreen.append({"text": newWord, 
                            "x": 0, "y": random.randint(50, screenHeight - 100), 
                            "color": "gray"})

def moveWords(screenWidth, wordsOnScreen, speed):

    for word in wordsOnScreen:
        word["x"] += speed
        wordWidth = font.size(word["text"])[0]

        if word["x"]  + wordWidth >= screenWidth and word["color"] == "gray":
            return True
    return False


def drawWords(screen, wordsOnScreen, font):
        
        for word in wordsOnScreen:
            wordDisplay = font.render(word["text"], True, word["color"])
            screen.blit(wordDisplay, (word["x"], word["y"]))

# Main game loop
while running:
    
    currentTime = pygame.time.get_ticks() # Ticks are in milliseconds
    
    if gameState == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                resizeWindow(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.collidepoint(convertToGamePosition(event.pos)):
                    gameState = "game"
                    lastWordSpawn = currentTime

        drawMenu(screen, titleFont, font, playButton)
    
    elif gameState == "game":

        screen.blit(gameBackground, (0, 0))

        results = eventHandler(wordsOnScreen, textbox, userText, active, score)
        running = results[0]
        userText = results[1]
        active = results[2]
        score = results[3]
        
        if currentTime - lastWordSpawn >= wordSpawnTime:
            spawnWord(words, wordsOnScreen)
            lastWordSpawn = currentTime

        
        missedWord = moveWords(screenWidth, wordsOnScreen, speed)
        if missedWord:
            gameState = "gameover"
        drawWords(screen, wordsOnScreen, font)
        drawtextbox(screen, textbox, userText, active, placeholderText)
        drawScore(screen, font, score)

    elif gameState == "gameover":

        screen.blit(gameBackground, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tryAgainButton.collidepoint(convertToGamePosition(event.pos)):
                    gameState = "game"
                    wordsOnScreen.clear()
                    userText = ""
                    active = False
                    score = 0
                    lastWordSpawn = currentTime
            if event.type == pygame.MOUSEBUTTONDOWN:
                if returnButton.collidepoint(convertToGamePosition(event.pos)):
                    gameState = "menu"
                    wordsOnScreen.clear()
                    userText = ""
                    active = False
                    score = 0
                    lastWordSpawn = currentTime
                    

        drawGameOver(screen, titleFont, font, tryAgainButton, returnButton, wordsOnScreen)

    scaledScreen = pygame.transform.scale(screen, window.get_size())
    window.blit(scaledScreen, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()