########## Imports from elsewhere
import pygame
from pygame.locals import *
import random
from random import *
import math
from math import *
import os
import string

#optional features for later:
    #checkpoints
    #best level beaten this session
    #colorful sparkles on walls
    #background starfield

fakeUpPress=pygame.event.Event(KEYDOWN,{"key":K_UP})
fakeDownPress=pygame.event.Event(KEYDOWN,{"key":K_DOWN})

class screen:
    #runs at start of screen, conducts background setup before first loop
    def __init__(self,xDim,yDim,playerHitboxHeight,playerHitboxWidth):
        pygame.init()
        self.screenSize=(xDim,yDim)
        self.playerHitboxHeight=playerHitboxHeight
        self.playerHitboxWidth=playerHitboxWidth
        self.gameScreen=pygame.display.set_mode(self.screenSize,0,32)
        self.backgroundColor=pygame.Color(0,0,0)
        self.gameScreen.fill(self.backgroundColor)
        self.gameSlice=pygame.Surface(self.screenSize)
        self.clock=pygame.time.Clock()
        self.fps=36
        self.playerPos=yDim/2
        #Initial y position of the top left corner of the player
        #(x position doesn't change).
        self.playerHitboxTop=self.playerPos
        self.playerHitboxBottom=self.playerPos+playerHitboxHeight
        self.playerHitboxLeft=xDim/2-playerHitboxWidth
        self.playerHitboxRight=xDim/2
        self.borders=self.generateBorders()
        self.level=self.getLevel()
        #self.level=1 #PUT THIS BACK
        self.hurdles=[self.generateHurdle()]
        self.pixelsSinceLastHurdle=0
        self.lives=3
        self.crash=False #make this true while announcing a crash
        self.running=True

        #The following needs to be the last line in __init__!
        self.mainloop()

    def mainloop(self):
        while self.running:
            event=self.getInput()
            self.processInput(event)
            self.drawScreen()
            self.clock.tick(self.fps)
        pygame.display.quit() #after you quit and running turns off, the while will exit and the display will quit


    def getLevel(self):
        #probably rejigger this to be controllable by EMG
        acceptable=[1,2,3,4,5,6,7,8,9,10]
        playerInput=""
        while playerInput not in acceptable:
            playerInput=input("Select a difficulty level between 1 and 10 inclusive.")
        return playerInput 


    def generateBorders(self):
        topBorder=pygame.Rect(0,0,self.screenSize[0],20)#(left top width height)
        bottomBorder=pygame.Rect(0,self.screenSize[1]-20,self.screenSize[0],20)
        return [topBorder,bottomBorder]

    def generateHurdle(self):
        level=self.level
        wallGray=pygame.Color(188,188,188)
        gapSize=self.screenSize[0]-80-25*level
        topOfGap=randint(20,self.screenSize[1]-gapSize)
        bottomOfGap=topOfGap+gapSize
        aboveGap=pygame.Surface((30,topOfGap))
        aboveGap.fill(wallGray)
        belowGap=pygame.Surface((30,self.screenSize[1]-bottomOfGap))
        belowGap.fill(wallGray)
        return [aboveGap,belowGap,self.screenSize[0]-30,bottomOfGap]
        #top surface, bottom surface, x coordinate of left, y coordinate of bottom of gap
        
    def getInput(self):
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                self.running=False
            else:
                #add some screening for the right type of input here
                return event
        #wait to write the rest until you have inputs

    def processInput(self,event):
        #this will probably change when you have inputs
        if not event:
            return
        if event is fakeUpPress:
            self.playerPos-=1
        elif event is fakeDownPress:
            self.playerPos+=1
        self.advanceScreen()

    def advanceScreen(self):
        for hurdle in self.hurdles:
            hurdle[2]-=1
        if self.pixelsSinceLastHurdle>=spaceBetweenHurdles:
            self.pixelsSinceLastHurdle=0
            self.hurdles.append(self.generateHurdle())
        self.pixelsSinceLastHurdle+=1
                

    def drawScreen(self):
        self.backgroundColor=pygame.Color(0,0,0)
        self.gameScreen.fill(self.backgroundColor)
        wallGray=pygame.Color(188,188,188)
        for border in self.borders:
            pygame.draw.rect(self.gameScreen, wallGray, border)
        for hurdle in self.hurdles:
            topPos=(hurdle[2],20)
            bottomPos=(hurdle[2],hurdle[3])
            self.gameScreen.blit(hurdle[0],topPos)
            self.gameScreen.blit(hurdle[1],bottomPos)
            #pygame.draw.rect(self.gameScreen, wallGray, hurdle[0])
            #pygame.draw.rect(self.gameScreen, wallGray, hurdle[1])
        tempShipColor=pygame.Color(0,0,255)
        spaceship=pygame.Rect(self.playerHitboxLeft,self.playerHitboxTop,self.playerHitboxWidth,self.playerHitboxHeight)
        pygame.draw.rect(self.gameScreen,tempShipColor,spaceship)
        pygame.display.flip()


screenWidth=500
screenHeight=500
playerHitboxHeight=50
playerHitboxWidth=100
spaceBetweenHurdles=200 #make this change with level?
game=screen(screenWidth,screenHeight,playerHitboxHeight,playerHitboxWidth) #START
