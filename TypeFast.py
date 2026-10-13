import pygame
import random

pygame.init()
pygame.key.set_repeat(400,50)

screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True

gameState = "menu"

titleFont = pygame.font.Font(None, 100)
font = pygame.font.Font(None, 50)

words = ["APPROXIMATE", "TEMPERATURE", "SUPERFLUOUS", 
         "FAVORABLE", "DECISIVE", "CYCLICAL", 
         "HUMOROUS", "INCONSPICUOUS", "XYLOPHONE", 
         "JUXTAPOSE", "KANGAROO", "LUMINOUS", 
         "METICULOUS", "NOSTALGIA", "OBLIVIOUS", 
         "PERSISTENT", "QUINTESSENTIAL"]

speed = 5
wordSpawnTime = 2000 # This is in milliseconds, so 2000ms = 2 seconds
lastWordSpawn = 0
wordsOnScreen = []

textBoxWidth = (screenWidth - 600) // 2
textBoxHeight = screenHeight - 80
textBox = pygame.Rect(textBoxWidth,textBoxHeight, 600, 50)
textBoxFont = pygame.font.Font(None, 30)
userText = ""
active = False
placeholderText = "Type fast before the word reaches the end!"


# Menu Setup
playButton = pygame.Rect((screenWidth - 200) // 2, (screenHeight - 50) // 2, 200, 50)

def drawMenu(screen, titleFont, font, playButton):
    screen.fill("black")
    titleFont = pygame.font.Font(None, 100)
    titleText = titleFont.render("TypeFast", True, "white")
    titleRect = titleText.get_rect(center=(screenWidth // 2, 200))
    screen.blit(titleText, titleRect)

    if playButton.collidepoint(pygame.mouse.get_pos()):
        buttonColor = "white"
    else:
        buttonColor = "skyblue"

    pygame.draw.rect(screen, buttonColor, playButton, border_radius = 10)

    playText = font.render("Play", True, "black")
    playTextRect = playText.get_rect(center=playButton.center)
    screen.blit(playText, playTextRect)

# Game Over Setup

tryAgainButton = pygame.Rect((screenWidth - 200) // 2, (screenHeight - 50) // 2 + 100, 200, 50)

exitButton = pygame.Rect((screenWidth - 200) // 2, (screenHeight - 50) // 2 + 200, 200, 50)

def drawGameOver(screen, titleFont, font, wordsOnScreen):
    screen.fill("black")
    drawWords(screen, wordsOnScreen, font)

    gameOverText = titleFont.render("Game Over", True, "white")
    gameOverRect = gameOverText.get_rect(center=(screenWidth // 2, screenHeight // 2))
    screen.blit(gameOverText, gameOverRect)

    pygame.draw.rect(screen, "white", tryAgainButton, border_radius = 10)
    tryAgainText = font.render("Try Again", True, "black")
    tryAgainTextRect = tryAgainText.get_rect(center=tryAgainButton.center)
    screen.blit(tryAgainText, tryAgainTextRect)

    pygame.draw.rect(screen, "white", exitButton, border_radius = 10)
    exitText = font.render("Exit", True, "black")
    exitTextRect = exitText.get_rect(center=exitButton.center)
    screen.blit(exitText, exitTextRect)

def eventHandler(wordsOnScreen, textBox, userText, active):
    
    running = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if textBox.collidepoint(event.pos):
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_BACKSPACE:
                userText = userText[:-1]
            # Checks if the user typed the correct word
            elif event.key == pygame.K_RETURN:
                for word in wordsOnScreen:
                    if word["text"] == userText and word["color"] == "white":
                        word["color"] = "skyblue"
                        break
                userText = ""
            else:
                userText += event.unicode.upper()
    return running, userText, active
    

def drawTextBox(screen, textBox, userText, active, placeholderText):

    pygame.draw.rect(screen, "white", textBox, 2, border_radius = 10)
    if userText == "" and not active:
        boxText = textBoxFont.render(placeholderText, True, "grey")
    else:
        boxText = textBoxFont.render(userText, True, "white")

    screen.blit(boxText, (textBox.x + 10, textBox.y + 15))

def spawnWord(words, wordsOnScreen):

    newWord = random.choice(words)
    wordsOnScreen.append({"text": newWord, 
                            "x": 0, "y": random.randint(50, 500), 
                            "color": "white"})

def moveWords(screenWidth, wordsOnScreen, speed):

    for word in wordsOnScreen:
        word["x"] += speed
        wordWidth = font.size(word["text"])[0]

        if word["x"]  + wordWidth >= screenWidth and word["color"] == "white":
            word["color"] = "red"
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.collidepoint(event.pos):
                    gameState = "game"
                    lastWordSpawn = currentTime

        drawMenu(screen, titleFont, font, playButton)
    
    elif gameState == "game":

        results = eventHandler(wordsOnScreen, textBox, userText, active)
        running = results[0]
        userText = results[1]
        active = results[2]
        
        if currentTime - lastWordSpawn >= wordSpawnTime:
            spawnWord(words, wordsOnScreen)
            lastWordSpawn = currentTime

        screen.fill("black")
        
        missedWord = moveWords(screenWidth, wordsOnScreen, speed)
        if missedWord:
            gameState = "gameover"
        drawWords(screen, wordsOnScreen, font)
        drawTextBox(screen, textBox, userText, active, placeholderText)

    elif gameState == "gameover":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tryAgainButton.collidepoint(event.pos):
                    gameState = "game"
                    wordsOnScreen.clear()
                    userText = ""
                    active = False
                    lastWordSpawn = currentTime
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exitButton.collidepoint(event.pos):
                    gameState = "menu"
                    wordsOnScreen.clear()
                    userText = ""
                    active = False
                    lastWordSpawn = currentTime
                    

        drawGameOver(screen, titleFont, font, wordsOnScreen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()