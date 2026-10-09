import pygame
import random

pygame.init()
pygame.key.set_repeat(400,50)

screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True

words = ["APPROXIMATE", "TEMPERATURE", "SUPERFLUOUS", "FAVORABLE", "DECISIVE", "CYCLICAL", "HUMOROUS", "INCONSPICUOUS", "XYLOPHONE", "JUXTAPOSE", "KANGAROO", "LUMINOUS", "METICULOUS", "NOSTALGIA", "OBLIVIOUS", "PERSISTENT", "QUINTESSENTIAL", "RANDOMIZE", "SYNCHRONIZE", "TRANSCENDENTAL", "UNIVERSAL", "VINDICATE", "WHIMSICAL", "XENOPHOBIA", "YOUTHFUL", "ZEALOUS"]
currentWord = random.choice(words)
font = pygame.font.Font(None, 50)
speed = 8
x = 0
y = random.randint(100, screenHeight)


textBoxWidth = (screenWidth - 600) // 2
textBoxHeight = screenHeight - 80
textBox = pygame.Rect(textBoxWidth,textBoxHeight, 600, 50)
textBoxFont = pygame.font.Font(None, 30)
userText = ""
active = False
placeholderText = "Type fast before the word reaches the end!"
    
displayWord = font.render(currentWord, True, "white")

while running:
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
                if userText.upper() == currentWord:
                        currentWord = random.choice(words)
                        displayWord = font.render(currentWord, True, "white")
                        userText = ""
                        x = 0
                        y = random.randint(100, screenHeight)
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
    
    # Moving word across the screen
    movingWord = screen.blit(displayWord, (x, y))
    x += speed 
    if x == screenWidth:
        currentWord = random.choice(words)
        displayWord = font.render(currentWord, True, "white")
        x = 0
        y = random.randint(100, screenHeight)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()