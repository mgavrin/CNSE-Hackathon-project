########## Imports from elsewhere
import pygame
from pygame.locals import *
import random
from random import *
import math
from math import *
import os
import string
import csv

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
    def __init__(self,xDim,yDim,playerHitboxHeight,playerHitboxWidth,debug=False):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        print pygame.mixer.get_init()
        self.screenSize=(xDim,yDim)
        self.gameScreen=pygame.display.set_mode(self.screenSize,0,32)
        self.backgroundColor=pygame.Color(0,0,0)
        self.mainFont=pygame.font.SysFont("arial",25)
        self.mainFont.set_bold(True)
        self.gameScreen.blit(backgroundImage,(0,0))
        self.gameSlice=pygame.Surface(self.screenSize)
        self.clock=pygame.time.Clock()
        self.fps=720
        self.debug=debug#true when hardware is not connected
        self.playerHitboxHeight=playerHitboxHeight
        self.playerHitboxWidth=playerHitboxWidth
        self.playerPos=yDim/2
        #Initial y position of the top left corner of the player
        #(x position doesn't change).
        self.getHitbox()
        self.borders=self.generateBorders()
        if not debug:
            self.emgSetup()
            self.level=self.getLevel()
            self.lives=3
        else:
            self.level=1
            self.lives=1
        #firstHurdle=hurdle(yDim,self.level)
        self.hurdles=[]
        self.calibrationPeriod=True
        self.pixelsSinceLastHurdle=175
        self.hurdlesPassed=-1
        #compensate for the absence-of-hurdle during the calibration period
        self.hurdlesPassedThisLevel=0
        self.allObstacles=[]
        self.crashedObstacles=[]
        self.relaxing=False #initial calibration period
        self.crash=False #make this true while announcing a crash
        self.gameOver=False
        self.paused=False
        self.allPreviousData=[]
        self.crashSound=pygame.mixer.Sound(os.path.join("Art","crash sound.wav"))
        self.gameOverSound=pygame.mixer.Sound(os.path.join("Art","game over sound.wav"))
        self.BGM=pygame.mixer.Sound(os.path.join("Art","BGM3.wav"))
        self.BGM.play(-1)
        self.running=True

        #The following needs to be the last line in __init__!
        self.mainloop()

    def mainloop(self):
        counter=0
        while self.running:
            if not self.debug:
                data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                if data[10]==")":
                    datumNumber=data[9]
                    datum=data[12:]
                else:
                    datumNumber=data[9:11]
                    datum=data[13:]
                self.allPreviousData.append(datum)
            counter+=1
            if counter%50==0:
                event=self.getInput()
                if not self.paused:
                    self.processInput(event)
                    self.updateGameState()
                    self.drawScreen()
                    self.clock.tick(self.fps)
        
        with open('eggs.csv', 'wb') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
                datawriter.writerow([allPreviousData])
        pygame.display.quit() #after you quit and running turns off, the while will exit and the display will quit
        
    def emgSetup(self):   
        import socket
   
        UDP_IP = "127.0.0.1"
        UDP_PORT = 20101
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.sock.bind((UDP_IP, UDP_PORT))
   


    def getHitbox(self):
        hitboxTop=self.playerPos
        hitboxLeft=self.screenSize[0]/2-self.playerHitboxWidth
        self.playerHitboxRect=pygame.Rect(hitboxLeft,hitboxTop,playerHitboxWidth,playerHitboxHeight)
    
    def getLevel(self):
        acceptable=range(1,10)
        playerInput=""
        while playerInput not in acceptable:
            playerInput=input("Select a difficulty level between 1 and 10 inclusive.")
        return playerInput 


    def generateBorders(self):
        topBorder=pygame.Rect(0,0,self.screenSize[0],20)#(left top width height)
        bottomBorder=pygame.Rect(0,self.screenSize[1]-20,self.screenSize[0],20)
        return [topBorder,bottomBorder]
        
    def getInput(self):
        events=pygame.event.get()
        if self.debug:
            data="Signal(0,0) 00"
        else:
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
        print "data:",data
        if "Signal" in data and len(data)>=13 and int(data[7])==activeChannel:
            print "found some data"
            channel=data[7]
            if data[10]==")":
                datumNumber=data[9]
                datum=data[12:]
            else:
                datumNumber=data[9:11]
                datum=float(data[13:])
            absDatum=abs(datum)
            print absDatum
            if absDatum>=0.1:
                events.append(fakeUpPress)
            else:
                events.append(fakeDownPress)
            self.allPreviousData.append(datum)
        for event in events:
            if event.type == QUIT:
                self.running=False
                print self.allPreviousData
            elif event.type==KEYDOWN and event.key==K_p:
                self.paused=not self.paused
            elif event in [fakeUpPress,fakeDownPress]:
                return event
            return None

    def processInput(self,event):
        if not event:
            return
        if event is fakeUpPress:
            self.playerPos=max(self.playerPos-1,0)
        elif event is fakeDownPress:
            self.playerPos=min(self.playerPos+1,self.screenSize[1])
        self.getHitbox()

    def updateGameState(self):
        self.advanceScreen()
        self.allObstacles=self.getAllObstacles()
        self.detectCrash()
        if self.hurdlesPassedThisLevel>15:
            self.hurdlesPassedThisLevel=0
            self.levelUp()

    def advanceScreen(self):
        for h in self.hurdles:
            h.aboveGapRect.left-=1
            h.belowGapRect.left-=1
        print self.pixelsSinceLastHurdle
        if self.pixelsSinceLastHurdle>=spaceBetweenHurdles:
            self.calibrationPeriod=False
            self.pixelsSinceLastHurdle=0
            self.hurdlesPassed+=1
            self.hurdlesPassedThisLevel+=1
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
        if self.gameOver:
            shipImage=gameOver
            shipBlitPos=(0,self.screenSize[1]/2-100)
        elif self.crash:
            shipImage=crashedShip
            shipBlitPos=self.playerHitboxRect.topleft
        elif self.calibrationPeriod:
            shipImage=self.mainFont.render("Squeeze . . .",False,(255,255,255))
            shipBlitPos=self.playerHitboxRect.topleft
        else:
            shipImage=aliveShip
            shipBlitPos=self.playerHitboxRect.topleft
        self.gameScreen.blit(shipImage,shipBlitPos)
        levelImg=self.mainFont.render("Level "+str(self.level),False,(255,255,255))
        livesImg=self.mainFont.render("Lives Remaining: "+str(self.lives),False,(255,255,255))
        scoreImg=self.mainFont.render("Score: "+str(self.hurdlesPassed),False,(255,255,255))
        self.gameScreen.blit(levelImg,(0,20))
        self.gameScreen.blit(livesImg,(245,20))
        self.gameScreen.blit(scoreImg,(0,self.screenSize[1]-45))
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
            self.crashSound.play()
            if self.lives==0:
                print "GAME OVER"
                self.gameOver=True
                self.paused=True
                self.BGM.stop()
                self.gameOverSound.play()
        elif collision==-1:
            self.crash=False

    def levelUp(self):
        print "Level up!"
        #add fancy on-screen stuff here
        self.level+=1

activeChannel=0 #the EMG channel that has data coming in
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
crashedShip=pygame.transform.scale(crashedShipImage, (playerHitboxWidth, playerHitboxHeight))
gameOver=pygame.image.load(os.path.join("Art","game over.png"))
backgroundImage=pygame.image.load(os.path.join("Art","Hubble_2004_Deep_Sky.jpg"))
backgroundImage=pygame.transform.scale(backgroundImage,(screenWidth,screenHeight))
game=screen(screenWidth,screenHeight,playerHitboxHeight,playerHitboxWidth,True) #START
