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

def main():
    pygame.init()
    global DISPLAYSURF
    FPSCLOCK=pygame.time.Clock()
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Game of Life')
    DISPLAYSURF.fill(WHITE)
    lifeDict=blankGrid()
    lifeDict=startingRandom(lifeDict)
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

if __name__=='__main__':
    main()