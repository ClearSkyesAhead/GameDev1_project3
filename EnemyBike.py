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
#from direct.showbase import DirectObject
import sys, math, random

from panda3d.ai import *

class EnemyBike(Bike):
    def __init__(self, cTrav, cevent):
        #messenger.toggleVerbose()
        Bike.__init__(self, cTrav)
        self.bike.setPos(0, 0, 10)
        self.initAI()
        
        frombikemask = BitMask32(0x10)
        intobikemask = BitMask32.allOff()
        floormask = BitMask32(0x2)
        
        self.cevent = CollisionHandlerEvent()
        self.cevent.addInPattern('%fn-into-%in')
        self.cevent.addOutPattern('%fn-out-%in')
        
        self.bullettrace = self.gun1.attachNewNode(CollisionNode('aimtrace'))
        self.bullettrace.node().addSolid(CollisionRay(0, 0, 0, 0, 1, 0))
        self.bullettrace.node().setFromCollideMask(frombikemask)
        self.bullettrace.node().setIntoCollideMask(intobikemask)
        self.bullettrace.show()
        #base.cTrav.addCollider(self.bullettrace, self.bike)
        base.cTrav.addCollider(self.bullettrace, self.cevent)
        
        self.gravtrace = self.bike.attachNewNode(CollisionNode('colNode'))
        self.gravtrace.node().addSolid(CollisionRay(0, 0, 0, 0, 0, -1))
        self.gravtrace.node().setFromCollideMask(floormask)
        self.gravtrace.node().setIntoCollideMask(BitMask32.allOff())
        self.gravtrace.show()
        
        self.vistrace = self.bike.attachNewNode(CollisionNode('vistrace'))
        self.vistrace.node().addSolid(CollisionRay(0, 0, 0, 0, 1, 0))
        self.vistrace.node().addSolid(CollisionRay(0, 0, 0, 1, 1, 0))
        self.vistrace.node().addSolid(CollisionRay(0, 0, 0, -1, 1, 0))
        self.vistrace.node().addSolid(CollisionRay(0, 0, 0, 1, 1, .1))
        self.vistrace.node().addSolid(CollisionRay(0, 0, 0, -1, 1, .1))
        self.vistrace.node().setFromCollideMask(frombikemask)
        self.vistrace.node().setIntoCollideMask(intobikemask)
        self.vistrace.show()
        #base.cTrav.addCollider(self.vistrace, self.bike)
        base.cTrav.addCollider(self.vistrace, self.cevent)
         
        self.lifter = CollisionHandlerFloor()
        self.lifter.setMaxVelocity(9.8)
        base.cTrav.addCollider(self.gravtrace,self.lifter)
        self.lifter.addCollider(self.gravtrace, self.bike)
        
        
        
        
        self.do = DirectObject()
        self.do.accept('vistrace-into-p_bike_push', self.visIn)
        self.do.accept('vistrace-out-p_bike_push', self.visOut)
		
    def initAI(self):
        self.AIchar = AICharacter("Enemy Bike", self.bike, 100, 0.05, 10)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        
        self.AImode = 'scan'
        
        #self.AIbehaviors.pursue(self.p_bike.bike, 0.7)
        #self.AIbehaviors.wander(1.0, 0, 30.0, 0.5)
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
            self.bullet.createBullet(self.bike)
            self.shotClock = 0
        else:
            self.shotClock += 1
            
    def aimIn(self, event):
        print length(self.bike.getPos(), event.getFromNodePath().getPos())
        self.AImode = 'target'
        #print event.getFromNodePath().getParent().AImode
        #print event
        
    def aimOut(self, event):
        print event

    def visIn(self, event):
        print self.physNode.getPos()
        #print self.bike.getPos()
        #print event.getIntoNodePath().getPos()
        #print event.getFromNodePath().getPos()
        print (self.bike.getPos() - event.getIntoNodePath().getPos()).length()
        #print self.AImode
        #print event.getFromNodePath().getParent().AImode
        #print event
        
    def visOut(self, event):
        print event
          