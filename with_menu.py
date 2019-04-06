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
WINDOWHEIGHT=850
CELLSIZE=10
assert WINDOWWIDTH % CELLSIZE == 0
assert WINDOWHEIGHT % CELLSIZE == 0
CELLWIDTH=WINDOWWIDTH//CELLSIZE
CELLHEIGHT=WINDOWHEIGHT//CELLSIZE

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

def startingRandom(lifeDict):
    for item in lifeDict:
        lifeDict[item] = random.randint(0,1)
    return lifeDict

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

def runLife(lifeDict):
    for item in lifeDict:
        colorGrid(item, lifeDict)
    drawGrid()
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        lifeDict=tick(lifeDict)
        for item in lifeDict:
            colorGrid(item, lifeDict)
        drawGrid()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def playRandom(lifeDict):
    lifeDict = startingRandom(lifeDict)
    runLife(lifeDict)
def patternSelect(argument=None):
    DISPLAYSURF.blit(titlescreen, (0, 0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        TextSurf, TextRect = text_color("Choose pattern", titleText,WHITE)
        TextRect.center = ((WINDOWWIDTH / 2), (WINDOWHEIGHT / 8))
        DISPLAYSURF.blit(TextSurf, TextRect)

        button('Glider',150,200,300,80,YELLOW,HIGH_YELLOW,BLACK)
        button('Pulsar', 150, 325, 300, 80, YELLOW, HIGH_YELLOW, BLACK)
        button('Glider Gun', 150, 450, 300, 80, YELLOW, HIGH_YELLOW, BLACK)
        button('-', 150, 575, 300, 80, YELLOW, HIGH_YELLOW, BLACK)
        button('-', 150, 700, 300, 80, YELLOW, HIGH_YELLOW, BLACK)
        button('Lightweight Spaceship', 550, 200, 300, 80, YELLOW, HIGH_YELLOW, BLACK)
        button('Pentadecathlon', 550, 325, 300, 80, YELLOW, HIGH_YELLOW, BLACK)
        button('-', 550, 450, 300, 80, YELLOW, HIGH_YELLOW, BLACK)
        button('-', 550, 575, 300, 80, YELLOW, HIGH_YELLOW, BLACK)
        button('Back', 550, 700, 300, 80, RED, HIGH_RED, WHITE)

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

        button('Play random',35,350,200,75,GREEN,HIGH_GREEN,WHITE,playRandom,lifeDict)
        button('Choose pattern',400,660,200,75,BLUE,HIGH_BLUE,WHITE,patternSelect)
        button('Quit',765,350,200,75,RED,HIGH_RED,WHITE,quit)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()