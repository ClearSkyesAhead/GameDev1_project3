#enemy bike class

from Bike import Bike

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
from panda3d.ai import *
import sys, math, random



class EnemyBike(Bike):
    def __init__(self):
        Bike.__init__(self)
        self.initAI()
		
    def initAI(self):
        self.AIchar = AICharacter("Enemy Bike", self.bike, 100, 0.05, 5)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
 
        #self.AIbehaviors.pursue(self.p_bike.bike, 0.7)
        self.AIbehaviors.wander(5.0, 1, 10, 0.3)
        #self.AIbehaviors.obstacleAvoidance(1.0)
        #self.e_bike.loop("run")
		

		