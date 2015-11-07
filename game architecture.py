########## Imports from elsewhere
import pygame
from pygame.locals import *
import random
from random import *
import math
from math import *
import os
import string

class game:
    def __init__():
        self.level=self.getLevel()
        self.lives=3





fakeUpPress=pygame.event.Event(KEYDOWN,{"key":K_UP})
fakeDownPress=pygame.event.Event(KEYDOWN,{"key":K_DOWN})

class screen:
    #runs at start of screen, conducts background setup before first loop
    def __init__(self,xDim,yDim):
        pygame.init()
        self.screenSize=(xDim,yDim)
        self.gameScreen=pygame.display.set_mode(self.screenSize,0,32)
        self.backgroundColor=pygame.Color(255,255,255)
        self.gameScreen.fill(self.backgroundColor)
        self.gameSlice=pygame.Surface(self.screenSize)
        self.clock=pygame.time.Clock()
        self.fps=36
        self.playerPos=yDim/2 #Initial position [x,y] of the player.
        self.level=self.getLevel()
        self.lives=3
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
        acceptable=["1","2","3","4","5","6","7","8","9","10"]
        playerInput=""
        while playerInput not in acceptable:
                playerInput=input("Select a difficulty level between 1 and 10 inclusive.")
        
            
        
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
        elif event is fakeUpPress:
            self.playerPos-=1



screenWidth=500
screenHeight=500
game=screen(screenWidth,screenHeight) #START
