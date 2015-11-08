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
    #life counter (important)
    #checkpoints?
    #best level beaten this session
    #colorful sparkles on walls
    #background starfield

hurdleCode=open("hurdle.py")
exec(hurdleCode.read())

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
        self.mainFont=pygame.font.SysFont("arial",25)
        self.mainFont.set_bold(True)
        self.gameScreen.blit(backgroundImage,(0,0))
        self.gameSlice=pygame.Surface(self.screenSize)
        self.clock=pygame.time.Clock()
        self.fps=36
        self.playerPos=yDim/2
        #Initial y position of the top left corner of the player
        #(x position doesn't change).
        hitboxTop=self.playerPos
        hitboxLeft=xDim/2-playerHitboxWidth
        self.playerHitboxRect=pygame.Rect(hitboxLeft,hitboxTop,playerHitboxWidth,playerHitboxHeight)
        self.borders=self.generateBorders()
        self.level=self.getLevel()
        #self.level=1 #PUT THIS BACK
        firstHurdle=hurdle(yDim,self.level)
        self.hurdles=[firstHurdle]
        self.pixelsSinceLastHurdle=0
        self.lives=3
        self.hurdlesPassed=0
        self.allObstacles=[]
        self.crashedObstacles=[]
        self.crash=False #make this true while announcing a crash
        self.running=True

        #The following needs to be the last line in __init__!
        self.mainloop()

    def mainloop(self):
        while self.running:
            event=self.getInput()
            self.processInput(event)
            self.updateGameState()
            self.drawScreen()
            self.clock.tick(self.fps)
        pygame.display.quit() #after you quit and running turns off, the while will exit and the display will quit


    def getLevel(self):
        #probably rejigger this to be controllable by EMG
        acceptable=range(1,20)
        playerInput=""
        while playerInput not in acceptable:
            playerInput=input("Select a difficulty level between 1 and 10 inclusive.")
        return playerInput 


    def generateBorders(self):
        topBorder=pygame.Rect(0,0,self.screenSize[0],20)#(left top width height)
        bottomBorder=pygame.Rect(0,self.screenSize[1]-20,self.screenSize[0],20)
        return [topBorder,bottomBorder]
        
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

    def updateGameState(self):
        self.advanceScreen()
        self.allObstacles=self.getAllObstacles()
        self.detectCrash()
        if self.hurdlesPassed>=15:
            self.hurdlesPassed=0
            self.levelUp()

    def advanceScreen(self):
        for h in self.hurdles:
            h.aboveGapRect.left-=1
            h.belowGapRect.left-=1
        if self.pixelsSinceLastHurdle>=spaceBetweenHurdles:
            self.pixelsSinceLastHurdle=0
            self.hurdlesPassed+=1
            newHurdle=hurdle(self.screenSize[1],self.level)
            self.hurdles.append(newHurdle)
        self.pixelsSinceLastHurdle+=1
                

    def drawScreen(self):
        self.backgroundColor=pygame.Color(0,0,0)
        #self.gameScreen.fill(self.backgroundColor)
        self.gameScreen.blit(backgroundImage,(0,0))
        wallGray=pygame.Color(188,188,188)
        for border in self.borders:
            pygame.draw.rect(self.gameScreen, wallGray, border)
        for hurdle in self.hurdles:
            topPos=(hurdle.aboveGapRect.left,20)
            bottomPos=(hurdle.belowGapRect.left,hurdle.belowGapRect.top)
            self.gameScreen.blit(hurdle.aboveGapSurface,hurdle.aboveGapRect)
            self.gameScreen.blit(hurdle.belowGapSurface,hurdle.belowGapRect)
        if self.crash:
            shipImage=crashedShip
        else:
            shipImage=aliveShip
        self.gameScreen.blit(shipImage,self.playerHitboxRect.topleft)
        levelImg=self.mainFont.render("Level "+str(self.level),False,(255,255,255))
        livesImg=self.mainFont.render("Lives Remaining: "+str(self.lives),False,(255,255,255))
        self.gameScreen.blit(levelImg,(0,20))
        self.gameScreen.blit(livesImg,(245,20))
        pygame.display.flip()

    def getAllObstacles(self):
        allObstacles=[]
        for r in self.borders:
            allObstacles.append(r)
        for h in self.hurdles:
            allObstacles.append(h.aboveGapRect)
            allObstacles.append(h.belowGapRect)
        return allObstacles

    def detectCrash(self):
        collision=self.playerHitboxRect.collidelist(self.allObstacles)
        if collision!=-1 and self.allObstacles[collision] not in self.crashedObstacles:
            #crashed into a new obstacle
            self.crash=True
            self.crashedObstacles.append(self.allObstacles[collision])
            self.lives-=1
            print "CRASH!"
            #add fancy on-screen stuff here
            if self.lives==0:
                print "GAME OVER"
            #add fancy on-screen stuff here
                self.running=False
        elif collision==-1:
            self.crash=False

    def levelUp(self):
        print "Level up!"
        #add fancy on-screen stuff here
        self.level+=1

screenWidth=500
screenHeight=500
playerHitboxHeight=50
playerHitboxWidth=100
spaceBetweenHurdles=200 #make this change with level?
aliveShipColor=pygame.Color(0,0,255)
crashedShipColor=pygame.Color(255,0,0)
aliveShipImage=pygame.image.load(os.path.join("Art","rocket_flat.png"))
crashedShipImage=pygame.image.load(os.path.join("Art","crash_flat.png"))
aliveShip=pygame.transform.scale(aliveShipImage, (playerHitboxWidth, playerHitboxHeight))
lifeMarker=pygame.transform.scale(aliveShipImage, (playerHitboxWidth/2, playerHitboxHeight/2))
crashedShip=pygame.transform.scale(crashedShipImage, (playerHitboxWidth, playerHitboxHeight))
backgroundImage=pygame.image.load(os.path.join("Art","Hubble_2004_Deep_Sky.jpg"))
backgroundImage=pygame.transform.scale(backgroundImage,(screenWidth,screenHeight))
#big thank you to NASA and clipart.co
#for putting their pics in the public domain!
game=screen(screenWidth,screenHeight,playerHitboxHeight,playerHitboxWidth) #START
