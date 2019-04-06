# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 14:37:54 2017

@author: Jakub Semczyszyn
"""
import pygame, sys, random
from pygame.locals import *

#Display settings
FPS=10

#Size settings
WINDOWWIDTH=1000
WINDOWHEIGHT=760
CELLSIZE=10 #with current resolution available values are: 2, 4, 5, 8, 10, 20, 40
assert WINDOWWIDTH % CELLSIZE == 0
assert WINDOWHEIGHT % CELLSIZE == 0
CELLWIDTH=WINDOWWIDTH//CELLSIZE
CELLHEIGHT=WINDOWHEIGHT//CELLSIZE
halfW = CELLWIDTH // 2
halfH = CELLHEIGHT // 2

#Color definitions
WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
GRAY=(40, 40, 40)
BLUE=(32, 152, 223)
GREEN=(19, 135, 16)
YELLOW=(249, 237, 13)
RED=(201, 0, 42)
HIGH_BLUE=(0, 255, 255)
HIGH_RED=(255, 0, 20)
HIGH_GREEN=(0, 255, 0)
HIGH_YELLOW=(255, 255, 0)

titlescreen=pygame.image.load('titlescreen.jpg')

def text_color(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(text,x,y,w,h,col,h_col,text_col,action=None,argument=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(DISPLAYSURF, h_col, (x, y, w, h))
        if click[0]==1 and not action==None:
            action(argument)
    else:
        pygame.draw.rect(DISPLAYSURF, col, (x, y, w, h))

    buttonText = pygame.font.Font('SimpleLife.ttf', 25)
    textSurf, textRect = text_color(text, buttonText, text_col)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    DISPLAYSURF.blit(textSurf, textRect)

def drawGrid():
    for x in range (0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, GRAY, (x,0), (x,WINDOWHEIGHT))
    for y in range (0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, GRAY, (0,y), (WINDOWWIDTH,y))

def blankGrid():
    gridDict={}
    for y in range (CELLHEIGHT):
        for x in range (CELLWIDTH):
            gridDict[x,y]=0
    return gridDict

def colorGrid(item, lifeDict):
    x=item[0]*CELLSIZE
    y=item[1]*CELLSIZE
    if lifeDict[item]==1:
        pygame.draw.rect(DISPLAYSURF, BLUE, (x,y,CELLSIZE,CELLSIZE))
    else:
        pygame.draw.rect(DISPLAYSURF, WHITE, (x,y,CELLSIZE,CELLSIZE))
    return None

def countNeighbors(item, lifeDict):
    neighbors=0
    for x in range (-1,2):
        for y in range (-1,2):
            checkCell=(item[0]+x,item[1]+y)
            if checkCell[0]<CELLWIDTH and checkCell[0]>=0:
                if checkCell[1]<CELLHEIGHT and checkCell[1]>=0:
                    if lifeDict[checkCell]==1:
                        if not x==0 or not y==0:
                            neighbors+=1
    return neighbors

def tick(lifeDict):
    newTick={}
    for item in lifeDict:
        numberNeighbors = countNeighbors(item, lifeDict)
        if lifeDict[item]==1:
            if numberNeighbors<2:
                newTick[item]=0
            elif numberNeighbors>3:
                newTick[item]=0
            else:
                newTick[item]=1
        else:
            if numberNeighbors==3:
                newTick[item]=1
            else:
                newTick[item]=0
    return newTick

def endLoop(argument=None):
    global loopcontrol
    loopcontrol=False

def runLife(lifeDict):
    for item in lifeDict:
        colorGrid(item, lifeDict)
    drawGrid()
    pygame.display.update()
    pause=True
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause=True
                    while(pause):
                        pygame.time.wait(1)
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    pause=False
        lifeDict=tick(lifeDict)
        for item in lifeDict:
            colorGrid(item, lifeDict)
        drawGrid()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def playRandom(lifeDict):
    for item in lifeDict:
        lifeDict[item] = random.randint(0,1)
    runLife(lifeDict)

def playSelect(lifeDict):
    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    runLife(lifeDict)
        if click[0]==1:
            if lifeDict[mouse[0]//CELLSIZE,mouse[1]//CELLSIZE]==0:
                lifeDict[mouse[0]//CELLSIZE, mouse[1]//CELLSIZE]=1
            else:
                lifeDict[mouse[0]//CELLSIZE, mouse[1]//CELLSIZE]=0
            for item in lifeDict:
                colorGrid(item, lifeDict)
            drawGrid()
            pygame.display.update()
        pygame.time.wait(110)

def playGlider(lifeDict):
    lifeDict[0, 1] = 1
    lifeDict[1, 2] = 1
    lifeDict[2, 0] = 1
    lifeDict[2, 1] = 1
    lifeDict[2, 2] = 1
    runLife(lifeDict)

def playPulsar(lifeDict):
    lifeDict[halfW - 4, halfH - 6] = 1
    lifeDict[halfW - 3, halfH - 6] = 1
    lifeDict[halfW - 2, halfH - 6] = 1
    lifeDict[halfW + 2, halfH - 6] = 1
    lifeDict[halfW + 3, halfH - 6] = 1
    lifeDict[halfW + 4, halfH - 6] = 1
    lifeDict[halfW - 6, halfH - 4] = 1
    lifeDict[halfW - 1, halfH - 4] = 1
    lifeDict[halfW + 1, halfH - 4] = 1
    lifeDict[halfW + 6, halfH - 4] = 1
    lifeDict[halfW - 6, halfH - 3] = 1
    lifeDict[halfW - 1, halfH - 3] = 1
    lifeDict[halfW + 1, halfH - 3] = 1
    lifeDict[halfW + 6, halfH - 3] = 1
    lifeDict[halfW - 6, halfH - 2] = 1
    lifeDict[halfW - 1, halfH - 2] = 1
    lifeDict[halfW + 1, halfH - 2] = 1
    lifeDict[halfW + 6, halfH - 2] = 1
    lifeDict[halfW - 4, halfH - 1] = 1
    lifeDict[halfW - 3, halfH - 1] = 1
    lifeDict[halfW - 2, halfH - 1] = 1
    lifeDict[halfW + 2, halfH - 1] = 1
    lifeDict[halfW + 3, halfH - 1] = 1
    lifeDict[halfW + 4, halfH - 1] = 1
    lifeDict[halfW - 4, halfH + 1] = 1
    lifeDict[halfW - 3, halfH + 1] = 1
    lifeDict[halfW - 2, halfH + 1] = 1
    lifeDict[halfW + 2, halfH + 1] = 1
    lifeDict[halfW + 3, halfH + 1] = 1
    lifeDict[halfW + 4, halfH + 1] = 1
    lifeDict[halfW - 6, halfH + 2] = 1
    lifeDict[halfW - 1, halfH + 2] = 1
    lifeDict[halfW + 1, halfH + 2] = 1
    lifeDict[halfW + 6, halfH + 2] = 1
    lifeDict[halfW - 6, halfH + 3] = 1
    lifeDict[halfW - 1, halfH + 3] = 1
    lifeDict[halfW + 1, halfH + 3] = 1
    lifeDict[halfW + 6, halfH + 3] = 1
    lifeDict[halfW - 6, halfH + 4] = 1
    lifeDict[halfW - 1, halfH + 4] = 1
    lifeDict[halfW + 1, halfH + 4] = 1
    lifeDict[halfW + 6, halfH + 4] = 1
    lifeDict[halfW - 4, halfH + 6] = 1
    lifeDict[halfW - 3, halfH + 6] = 1
    lifeDict[halfW - 2, halfH + 6] = 1
    lifeDict[halfW + 2, halfH + 6] = 1
    lifeDict[halfW + 3, halfH + 6] = 1
    lifeDict[halfW + 4, halfH + 6] = 1
    runLife(lifeDict)

def playSpaceship(lifeDict):
    lifeDict[0, halfH-1] = 1
    lifeDict[3, halfH-1] = 1
    lifeDict[4, halfH] = 1
    lifeDict[0, halfH+1] = 1
    lifeDict[4, halfH+1] = 1
    lifeDict[1, halfH+2] = 1
    lifeDict[2, halfH+2] = 1
    lifeDict[3, halfH+2] = 1
    lifeDict[4, halfH+2] = 1
    runLife(lifeDict)

def playPentadecathlon(lifeDict):
    lifeDict[halfW - 3, halfH - 1] = 1
    lifeDict[halfW + 2, halfH - 1] = 1
    lifeDict[halfW - 5, halfH] = 1
    lifeDict[halfW - 4, halfH] = 1
    lifeDict[halfW - 2, halfH] = 1
    lifeDict[halfW - 1, halfH] = 1
    lifeDict[halfW, halfH] = 1
    lifeDict[halfW + 1, halfH] = 1
    lifeDict[halfW + 3, halfH] = 1
    lifeDict[halfW + 4, halfH] = 1
    lifeDict[halfW - 3, halfH + 1] = 1
    lifeDict[halfW + 2, halfH + 1] = 1
    runLife(lifeDict)

def playGlidergun(lifeDict):
    lifeDict[24, 0] = 1
    lifeDict[22, 1] = 1
    lifeDict[24, 1] = 1
    lifeDict[12, 2] = 1
    lifeDict[13, 2] = 1
    lifeDict[20, 2] = 1
    lifeDict[21, 2] = 1
    lifeDict[34, 2] = 1
    lifeDict[35, 2] = 1
    lifeDict[11, 3] = 1
    lifeDict[15, 3] = 1
    lifeDict[20, 3] = 1
    lifeDict[21, 3] = 1
    lifeDict[34, 3] = 1
    lifeDict[35, 3] = 1
    lifeDict[0, 4] = 1
    lifeDict[1, 4] = 1
    lifeDict[10, 4] = 1
    lifeDict[16, 4] = 1
    lifeDict[20, 4] = 1
    lifeDict[21, 4] = 1
    lifeDict[0, 5] = 1
    lifeDict[1, 5] = 1
    lifeDict[10, 5] = 1
    lifeDict[14, 5] = 1
    lifeDict[16, 5] = 1
    lifeDict[17, 5] = 1
    lifeDict[22, 5] = 1
    lifeDict[24, 5] = 1
    lifeDict[10, 6] = 1
    lifeDict[16, 6] = 1
    lifeDict[24, 6] = 1
    lifeDict[11, 7] = 1
    lifeDict[15, 7] = 1
    lifeDict[12, 8] = 1
    lifeDict[13, 8] = 1
    runLife(lifeDict)

def playCentinal(lifeDict):
    lifeDict[halfW - 26, halfH - 8] = 1
    lifeDict[halfW - 26, halfH + 8] = 1
    lifeDict[halfW - 25, halfH - 8] = 1
    lifeDict[halfW - 25, halfH - 7] = 1
    lifeDict[halfW - 25, halfH - 6] = 1
    lifeDict[halfW - 25, halfH + 6] = 1
    lifeDict[halfW - 25, halfH + 7] = 1
    lifeDict[halfW - 25, halfH + 8] = 1
    lifeDict[halfW - 24, halfH - 5] = 1
    lifeDict[halfW - 24, halfH + 5] = 1
    lifeDict[halfW - 23, halfH - 6] = 1
    lifeDict[halfW - 23, halfH - 5] = 1
    lifeDict[halfW - 23, halfH + 5] = 1
    lifeDict[halfW - 23, halfH + 6] = 1
    lifeDict[halfW - 16, halfH - 3] = 1
    lifeDict[halfW - 16, halfH + 3] = 1
    lifeDict[halfW - 15, halfH - 4] = 1
    lifeDict[halfW - 15, halfH - 3] = 1
    lifeDict[halfW - 15, halfH - 2] = 1
    lifeDict[halfW - 15, halfH + 2] = 1
    lifeDict[halfW - 15, halfH + 3] = 1
    lifeDict[halfW - 15, halfH + 4] = 1
    lifeDict[halfW - 14, halfH - 5] = 1
    lifeDict[halfW - 14, halfH - 4] = 1
    lifeDict[halfW - 14, halfH - 2] = 1
    lifeDict[halfW - 14, halfH + 2] = 1
    lifeDict[halfW - 14, halfH + 4] = 1
    lifeDict[halfW - 14, halfH + 5] = 1
    lifeDict[halfW - 11, halfH - 2] = 1
    lifeDict[halfW - 11, halfH + 2] = 1
    lifeDict[halfW - 10, halfH - 2] = 1
    lifeDict[halfW - 10, halfH + 2] = 1
    lifeDict[halfW - 1, halfH - 6] = 1
    lifeDict[halfW - 1, halfH - 5] = 1
    lifeDict[halfW - 1, halfH + 5] = 1
    lifeDict[halfW - 1, halfH + 6] = 1
    lifeDict[halfW, halfH - 6] = 1
    lifeDict[halfW, halfH - 5] = 1
    lifeDict[halfW, halfH + 5] = 1
    lifeDict[halfW, halfH + 6] = 1
    lifeDict[halfW + 13, halfH - 5] = 1
    lifeDict[halfW + 13, halfH - 4] = 1
    lifeDict[halfW + 13, halfH - 2] = 1
    lifeDict[halfW + 13, halfH + 2] = 1
    lifeDict[halfW + 13, halfH + 4] = 1
    lifeDict[halfW + 13, halfH + 5] = 1
    lifeDict[halfW + 14, halfH - 5] = 1
    lifeDict[halfW + 14, halfH - 2] = 1
    lifeDict[halfW + 14, halfH + 2] = 1
    lifeDict[halfW + 14, halfH + 5] = 1
    lifeDict[halfW + 15, halfH - 4] = 1
    lifeDict[halfW + 15, halfH - 3] = 1
    lifeDict[halfW + 15, halfH - 2] = 1
    lifeDict[halfW + 15, halfH + 2] = 1
    lifeDict[halfW + 15, halfH + 3] = 1
    lifeDict[halfW + 15, halfH + 4] = 1
    lifeDict[halfW + 22, halfH - 6] = 1
    lifeDict[halfW + 22, halfH - 5] = 1
    lifeDict[halfW + 22, halfH + 5] = 1
    lifeDict[halfW + 22, halfH + 6] = 1
    lifeDict[halfW + 23, halfH - 5] = 1
    lifeDict[halfW + 23, halfH + 5] = 1
    lifeDict[halfW + 24, halfH - 8] = 1
    lifeDict[halfW + 24, halfH - 7] = 1
    lifeDict[halfW + 24, halfH - 6] = 1
    lifeDict[halfW + 24, halfH + 6] = 1
    lifeDict[halfW + 24, halfH + 7] = 1
    lifeDict[halfW + 24, halfH + 8] = 1
    lifeDict[halfW + 25, halfH - 8] = 1
    lifeDict[halfW + 25, halfH + 8] = 1
    runLife(lifeDict)

def playPuffer(lifeDict):
    lifeDict[0, halfH - 11] = 1
    lifeDict[0, halfH - 7] = 1
    lifeDict[0, halfH - 6] = 1
    lifeDict[0, halfH + 11] = 1
    lifeDict[0, halfH + 7] = 1
    lifeDict[0, halfH + 6] = 1
    lifeDict[1, halfH - 10] = 1
    lifeDict[1, halfH - 7] = 1
    lifeDict[1, halfH - 6] = 1
    lifeDict[1, halfH + 10] = 1
    lifeDict[1, halfH + 7] = 1
    lifeDict[1, halfH + 6] = 1
    lifeDict[2, halfH - 10] = 1
    lifeDict[2, halfH - 7] = 1
    lifeDict[2, halfH + 10] = 1
    lifeDict[2, halfH + 7] = 1
    lifeDict[3, halfH - 10] = 1
    lifeDict[3, halfH + 10] = 1
    lifeDict[4, halfH - 10] = 1
    lifeDict[4, halfH - 5] = 1
    lifeDict[4, halfH - 4] = 1
    lifeDict[4, halfH - 2] = 1
    lifeDict[4, halfH + 10] = 1
    lifeDict[4, halfH + 5] = 1
    lifeDict[4, halfH + 4] = 1
    lifeDict[4, halfH + 2] = 1
    lifeDict[5, halfH - 13] = 1
    lifeDict[5, halfH - 10] = 1
    lifeDict[5, halfH - 4] = 1
    lifeDict[5, halfH - 3] = 1
    lifeDict[5, halfH - 2] = 1
    lifeDict[5, halfH + 13] = 1
    lifeDict[5, halfH + 10] = 1
    lifeDict[5, halfH + 4] = 1
    lifeDict[5, halfH + 3] = 1
    lifeDict[5, halfH + 2] = 1
    lifeDict[6, halfH - 12] = 1
    lifeDict[6, halfH - 11] = 1
    lifeDict[6, halfH - 10] = 1
    lifeDict[6, halfH - 3] = 1
    lifeDict[6, halfH + 12] = 1
    lifeDict[6, halfH + 11] = 1
    lifeDict[6, halfH + 10] = 1
    lifeDict[6, halfH + 3] = 1
    runLife(lifeDict)

def playSpider(lifeDict):
    lifeDict[0, halfH - 8] = 1
    lifeDict[0, halfH + 8] = 1
    lifeDict[1, halfH - 12] = 1
    lifeDict[1, halfH - 11] = 1
    lifeDict[1, halfH - 9] = 1
    lifeDict[1, halfH - 8] = 1
    lifeDict[1, halfH + 12] = 1
    lifeDict[1, halfH + 11] = 1
    lifeDict[1, halfH + 9] = 1
    lifeDict[1, halfH + 8] = 1
    lifeDict[2, halfH - 12] = 1
    lifeDict[2, halfH - 11] = 1
    lifeDict[2, halfH - 1] = 1
    lifeDict[2, halfH + 12] = 1
    lifeDict[2, halfH + 11] = 1
    lifeDict[2, halfH + 1] = 1
    lifeDict[3, halfH - 9] = 1
    lifeDict[3, halfH - 8] = 1
    lifeDict[3, halfH - 1] = 1
    lifeDict[3, halfH + 9] = 1
    lifeDict[3, halfH + 8] = 1
    lifeDict[3, halfH + 1] = 1
    lifeDict[4, halfH - 13] = 1
    lifeDict[4, halfH - 9] = 1
    lifeDict[4, halfH - 7] = 1
    lifeDict[4, halfH - 1] = 1
    lifeDict[4, halfH + 13] = 1
    lifeDict[4, halfH + 9] = 1
    lifeDict[4, halfH + 7] = 1
    lifeDict[4, halfH + 1] = 1
    lifeDict[5, halfH - 13] = 1
    lifeDict[5, halfH - 12] = 1
    lifeDict[5, halfH - 11] = 1
    lifeDict[5, halfH - 9] = 1
    lifeDict[5, halfH - 7] = 1
    lifeDict[5, halfH - 6] = 1
    lifeDict[5, halfH - 5] = 1
    lifeDict[5, halfH + 13] = 1
    lifeDict[5, halfH + 12] = 1
    lifeDict[5, halfH + 11] = 1
    lifeDict[5, halfH + 9] = 1
    lifeDict[5, halfH + 7] = 1
    lifeDict[5, halfH + 6] = 1
    lifeDict[5, halfH + 5] = 1
    lifeDict[6, halfH - 10] = 1
    lifeDict[6, halfH - 9] = 1
    lifeDict[6, halfH - 7] = 1
    lifeDict[6, halfH - 5] = 1
    lifeDict[6, halfH - 3] = 1
    lifeDict[6, halfH - 2] = 1
    lifeDict[6, halfH + 10] = 1
    lifeDict[6, halfH + 9] = 1
    lifeDict[6, halfH + 7] = 1
    lifeDict[6, halfH + 5] = 1
    lifeDict[6, halfH + 3] = 1
    lifeDict[6, halfH + 2] = 1
    lifeDict[7, halfH - 4] = 1
    lifeDict[7, halfH + 4] = 1
    runLife(lifeDict)

def patternSelect(lifeDict):
    DISPLAYSURF.blit(titlescreen, (0, 0))
    pygame.display.update()
    global loopcontrol
    loopcontrol=True
    while loopcontrol:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        TextSurf, TextRect = text_color("Choose pattern", titleText,WHITE)
        TextRect.center = ((WINDOWWIDTH / 2), (WINDOWHEIGHT / 8))
        DISPLAYSURF.blit(TextSurf, TextRect)

        button('Glider',100,200,300,80,YELLOW,HIGH_YELLOW,BLACK, playGlider, lifeDict)
        button('Pulsar', 100, 310, 300, 80, YELLOW, HIGH_YELLOW, BLACK, playPulsar, lifeDict)
        button('Glider Gun', 100, 420, 300, 80, YELLOW, HIGH_YELLOW, BLACK, playGlidergun, lifeDict)
        button('Centinal', 100, 530, 300, 80, YELLOW, HIGH_YELLOW, BLACK, playCentinal, lifeDict)
        button('Play random', 100, 640, 300, 80, BLUE, HIGH_BLUE, WHITE, playRandom, lifeDict)
        button('Lightweight Spaceship', 600, 200, 300, 80, YELLOW, HIGH_YELLOW, BLACK, playSpaceship, lifeDict)
        button('Pentadecathlon', 600, 310, 300, 80, YELLOW, HIGH_YELLOW, BLACK, playPentadecathlon, lifeDict)
        button('Puffer', 600, 420, 300, 80, YELLOW, HIGH_YELLOW, BLACK, playPuffer, lifeDict)
        button('Spider', 600, 530, 300, 80, YELLOW, HIGH_YELLOW, BLACK,playSpider, lifeDict)
        button('Back', 600, 640, 300, 80, RED, HIGH_RED, WHITE, endLoop)

        pygame.display.update()
    DISPLAYSURF.blit(titlescreen, (0, 0))
    pygame.display.update()

def main():
    pygame.init()
    global DISPLAYSURF
    global FPSCLOCK
    global titleText
    FPSCLOCK=pygame.time.Clock()
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Game of Life')
    DISPLAYSURF.blit(titlescreen,(0,0))
    lifeDict=blankGrid()
    titleText = pygame.font.Font('SimpleLife.ttf', 125)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        TextSurf, TextRect = text_color("Game of Life", titleText,WHITE)
        TextRect.center = ((WINDOWWIDTH / 2), (WINDOWHEIGHT / 8))
        DISPLAYSURF.blit(TextSurf, TextRect)

        button('Play',35,350,200,75,GREEN,HIGH_GREEN,WHITE,playSelect,lifeDict)
        button('Choose pattern',400,660,200,75,BLUE,HIGH_BLUE,WHITE,patternSelect,lifeDict)
        button('Quit',765,350,200,75,RED,HIGH_RED,WHITE,quit)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()