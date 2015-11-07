########## Imports from elsewhere
import pygame
from pygame.locals import *
import random
from random import *

class hurdle:
    def __init__(self,height,level):
        wallGray=pygame.Color(188,188,188)
        gapSize=height-80-25*level
        topOfGap=randint(20,height-40-gapSize)
        bottomOfGap=topOfGap+gapSize
        self.aboveGapSurface=pygame.Surface((30,topOfGap-20))
        self.aboveGapSurface.fill(wallGray)
        self.belowGapSurface=pygame.Surface((30,height-20-bottomOfGap))
        self.belowGapSurface.fill(wallGray)
        self.aboveGapRect=pygame.Rect(height-30,20,30,topOfGap-20)
        self.belowGapRect=pygame.Rect(height-30,
                                 topOfGap+gapSize,30,height-20-bottomOfGap)

        if 20+20+gapSize+self.belowGapRect.height+self.aboveGapRect.height!=height:
            print "You screwed up your math!"
            print 20+20+gapSize+self.belowGapRect.height+self.aboveGapRect.height
            print height
        elif 20+20+gapSize+self.belowGapSurface.get_height()+self.aboveGapSurface.get_height()!=height:
            print "You screwed up your math!"
        
            
