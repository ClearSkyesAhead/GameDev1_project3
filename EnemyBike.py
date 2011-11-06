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
from direct.showbase import DirectObject
import sys, math, random

from panda3d.ai import *

def inview():
    pass

class ViewCollider(DirectObject.DirectObject):
    def __init__(self):
        self.accept('vistrace-into-p_bike', inview);
        
    def inview(self, event):
        print entry

ViewCollider()

class AimCollider(DirectObject.DirectObject):
    def __init__(self):
        self.accept('aimtrace-into-p_bike', inview);
        
    def inview(self, event):
        print entry

AimCollider()
    

class EnemyBike(Bike):
    def __init__(self, cTrav, cevent):
        Bike.__init__(self, cTrav)
        self.bike.setPos(0, 0, 10)
        self.initAI()
        
        frombikemask = BitMask32(0x10)
        intobikemask = BitMask32.allOff()
        
        self.bullettracel = self.gun1.attachNewNode(CollisionNode('cnode'))
        self.bullettracel.node().addSolid(CollisionRay(0, 0, 0, 0, 1, 0))
        self.bullettracel.node().setFromCollideMask(frombikemask)
        self.bullettracel.node().setFromCollideMask(intobikemask)
        self.bullettracel.show()
        
        self.bullettracer = self.gun2.attachNewNode(CollisionNode('cnode'))
        self.bullettracer.node().addSolid(CollisionRay(0, 0, 0, 0, 1, 0))
        self.bullettracer.node().setFromCollideMask(frombikemask)
        self.bullettracer.node().setIntoCollideMask(intobikemask)
        self.bullettracer.show()
        
        self.gravtrace = self.bike.attachNewNode(CollisionNode('colNode'))
        self.gravtrace.node().addSolid(CollisionRay(0, 0, 0, 0, 0, -1))
        self.gravtrace.node().setFromCollideMask(BitMask32.allOff())
        self.gravtrace.node().setFromCollideMask(BitMask32.allOff())
        self.gravtrace.show()
        
        self.vistrace = self.bike.attachNewNode(CollisionNode('cnode'))
        self.vistrace.node().addSolid(CollisionRay(0, 0, 0, 0, 1, 0))
        self.vistrace.node().setFromCollideMask(frombikemask)
        self.vistrace.node().setIntoCollideMask(intobikemask)
        self.vistrace.show()
        
        self.vistracel = self.bike.attachNewNode(CollisionNode('cnode'))
        self.vistracel.node().addSolid(CollisionRay(0, 0, 0, 1, 1, 0))
        self.vistracel.node().setFromCollideMask(frombikemask)
        self.vistracel.node().setIntoCollideMask(intobikemask)
        self.vistracel.show()
        
        self.vistracer = self.bike.attachNewNode(CollisionNode('cnode'))
        self.vistracer.node().addSolid(CollisionRay(0, 0, 0, -1, 1, 0))
        self.vistracer.node().setFromCollideMask(frombikemask)
        self.vistracer.node().setIntoCollideMask(intobikemask)
        self.vistracer.show()
        
        self.vistraceul = self.bike.attachNewNode(CollisionNode('cnode'))
        self.vistraceul.node().addSolid(CollisionRay(0, 0, 0, 1, 1, .1))
        self.vistraceul.node().setFromCollideMask(frombikemask)
        self.vistraceul.node().setIntoCollideMask(intobikemask)
        self.vistraceul.show()
        
        self.vistraceur = self.bike.attachNewNode(CollisionNode('cnode'))
        self.vistraceur.node().addSolid(CollisionRay(0, 0, 0, -1, 1, .1))
        self.vistraceur.node().setFromCollideMask(frombikemask)
        self.vistraceur.node().setIntoCollideMask(intobikemask)
        self.vistraceur.show()
         
        self.lifter = CollisionHandlerFloor()
        self.lifter.setMaxVelocity(9.8)
        base.cTrav.addCollider(self.gravtrace,self.lifter)
        self.lifter.addCollider(self.gravtrace, self.bike)
		
    def initAI(self):
        self.AIchar = AICharacter("Enemy Bike", self.bike, 100, 0.05, 10)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        
        self.AImode = 'scan'
        
        #self.AIbehaviors.pursue(self.p_bike.bike, 0.7)
        self.AIbehaviors.wander(1.0, 0, 30.0, 0.5)
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
          