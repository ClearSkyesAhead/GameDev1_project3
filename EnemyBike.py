#enemy bike class

from Bike import Bike

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
from panda3d.core import *
from panda3d.physics import *
import sys, math, random

from panda3d.ai import *

class EnemyBike(Bike):
    def __init__(self):
        Bike.__init__(self)
        self.bike.setPos(0, 0, 10)
        self.initAI()
        
        self.bullettrace = self.gun1.attachNewNode(CollisionNode('cnode'))
        self.bullettrace.node().addSolid(CollisionRay(0, 0, 0, 0, 1, 0))
        self.bullettrace.show()
        
        self.gravtrace = self.bike.attachNewNode(CollisionNode('colNode'))
        self.gravtrace.node().addSolid(CollisionRay(0, 0, 0, 0, 0, -1))
        self.gravtrace.show()
         
        self.lifter = CollisionHandlerFloor()
        self.lifter.setMaxVelocity(9.8)
        base.cTrav.addCollider(self.gravtrace,self.lifter)
        self.lifter.addCollider(self.gravtrace, self.bike)
		
    def initAI(self):
        self.AIchar = AICharacter("Enemy Bike", self.bike, 100, 0.05, 10)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
 
        #self.AIbehaviors.pursue(self.p_bike.bike, 0.7)
        self.AIbehaviors.wander(10.0, 0, 10, 0.3)
        #self.AIbehaviors.obstacleAvoidance(1.0)
        #self.e_bike.loop("run")
		
    def update(self):
        self.shoot()
        """if self.lights:
            self.lightsOff()
        else:
            self.lightsOn()"""
            
    def shoot(self):
        
        
        if self.shotClock >= 25:
            #create a bullet
            self.bullet.createBullet(self.gun1, self.bike)
            self.shotClock = 0
        else:
            self.shotClock += 1        
          