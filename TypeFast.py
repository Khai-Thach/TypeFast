import pygame
import random

pygame.init()
pygame.key.set_repeat(400,50)

screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True

words = ["APPROXIMATE", "TEMPERATURE", "SUPERFLUOUS", 
         "FAVORABLE", "DECISIVE", "CYCLICAL", 
         "HUMOROUS", "INCONSPICUOUS", "XYLOPHONE", 
         "JUXTAPOSE", "KANGAROO", "LUMINOUS", 
         "METICULOUS", "NOSTALGIA", "OBLIVIOUS", 
         "PERSISTENT", "QUINTESSENTIAL"]

currentWord = random.choice(words)
font = pygame.font.Font(None, 50)
speed = 5
x = 0
y = random.randint(50, 500)
displayWord = font.render(currentWord, True, "white")
wordSpawnTime = 2000
lastWordSpawn = 0
wordsOnScreen = []

textBoxWidth = (screenWidth - 600) // 2
textBoxHeight = screenHeight - 80
textBox = pygame.Rect(textBoxWidth,textBoxHeight, 600, 50)
textBoxFont = pygame.font.Font(None, 30)
userText = ""
active = False
placeholderText = "Type fast before the word reaches the end!"
    


while running:
    currentTime = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if textBox.collidepoint(event.pos):
                active = True
            else:
                active = False
        # Checks if the user typed the correct word
        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_BACKSPACE:
                userText = userText[:-1]
            elif event.key == pygame.K_RETURN:
                for word in wordsOnScreen:
                    if word["text"] == userText and word["color"] == "white":
                        word["color"] = "blue"
                        word["currentTime"] = currentTime
                        break
                userText = ""
            else:
                userText += event.unicode.upper()


    screen.fill("black")

    # Load textbox for user to type in
    pygame.draw.rect(screen, "white", textBox, 2)
    if userText == "" and not active:
        boxText = textBoxFont.render(placeholderText, True, "grey")
    else:
        boxText = textBoxFont.render(userText, True, "white")
    screen.blit(boxText, (textBox.x + 10, textBox.y + 15))
    
    # Spawning multiple words on the screen
    if currentTime - lastWordSpawn >= wordSpawnTime:
        newWord = random.choice(words)
        newWordDisplay = font.render(newWord, True, "white")
        wordsOnScreen.append({"text": newWord, 
                              "display": newWordDisplay, 
                              "x": 0, "y": random.randint(50, 500), 
                              "color": "white"})
        lastWordSpawn = currentTime

    # Moving words across the screen
    for word in list(wordsOnScreen):
        word["x"] += speed
        wordDisplay = font.render(word["text"], True, word["color"])
        screen.blit(wordDisplay, (word["x"], word["y"]))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()