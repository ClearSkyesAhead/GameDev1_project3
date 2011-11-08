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

def visIn(event):
    print "!"
    print event
    
def visOut(event):
    print "?"
    print event

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
        
        self.bullettracel = self.gun1.attachNewNode(CollisionNode('aimtrace'))
        self.bullettracel.node().addSolid(CollisionRay(0, 0, 0, 0, 1, 0))
        self.bullettracel.node().setFromCollideMask(frombikemask)
        self.bullettracel.node().setIntoCollideMask(intobikemask)
        self.bullettracel.show()
        base.cTrav.addCollider(self.bullettracel, self.cevent)
        
        self.bullettracer = self.gun2.attachNewNode(CollisionNode('aimtrace'))
        self.bullettracer.node().addSolid(CollisionRay(0, 0, 0, 0, 1, 0))
        self.bullettracer.node().setFromCollideMask(frombikemask)
        self.bullettracer.node().setIntoCollideMask(intobikemask)
        self.bullettracer.show()
        base.cTrav.addCollider(self.bullettracer, self.cevent)
        
        self.gravtrace = self.bike.attachNewNode(CollisionNode('colNode'))
        self.gravtrace.node().addSolid(CollisionRay(0, 0, 0, 0, 0, -1))
        self.gravtrace.node().setFromCollideMask(floormask)
        self.gravtrace.node().setIntoCollideMask(BitMask32.allOff())
        self.gravtrace.show()
        
        self.vistrace = self.bike.attachNewNode(CollisionNode('vistrace'))
        self.vistrace.node().addSolid(CollisionRay(0, 0, 0, 0, 1, 0))
        self.vistrace.node().setFromCollideMask(frombikemask)
        self.vistrace.node().setIntoCollideMask(intobikemask)
        self.vistrace.show()
        base.cTrav.addCollider(self.vistrace, self.cevent)
        
        self.vistracel = self.bike.attachNewNode(CollisionNode('vistrace'))
        self.vistracel.node().addSolid(CollisionRay(0, 0, 0, 1, 1, 0))
        self.vistracel.node().setFromCollideMask(frombikemask)
        self.vistracel.node().setIntoCollideMask(intobikemask)
        self.vistracel.show()
        base.cTrav.addCollider(self.vistracel, self.cevent)
        
        self.vistracer = self.bike.attachNewNode(CollisionNode('vistrace'))
        self.vistracer.node().addSolid(CollisionRay(0, 0, 0, -1, 1, 0))
        self.vistracer.node().setFromCollideMask(frombikemask)
        self.vistracer.node().setIntoCollideMask(intobikemask)
        self.vistracer.show()
        base.cTrav.addCollider(self.vistracer, self.cevent)
        
        self.vistraceul = self.bike.attachNewNode(CollisionNode('vistrace'))
        self.vistraceul.node().addSolid(CollisionRay(0, 0, 0, 1, 1, .1))
        self.vistraceul.node().setFromCollideMask(frombikemask)
        self.vistraceul.node().setIntoCollideMask(intobikemask)
        self.vistraceul.show()
        base.cTrav.addCollider(self.vistraceul, self.cevent)
        
        self.vistraceur = self.bike.attachNewNode(CollisionNode('vistrace'))
        self.vistraceur.node().addSolid(CollisionRay(0, 0, 0, -1, 1, .1))
        self.vistraceur.node().setFromCollideMask(frombikemask)
        self.vistraceur.node().setIntoCollideMask(intobikemask)
        self.vistraceur.show()
        base.cTrav.addCollider(self.vistraceur, self.cevent)
         
        self.lifter = CollisionHandlerFloor()
        self.lifter.setMaxVelocity(9.8)
        base.cTrav.addCollider(self.gravtrace,self.lifter)
        self.lifter.addCollider(self.gravtrace, self.bike)
        
        
        self.cevent.addInPattern('%fn-into-%in')
        self.cevent.addOutPattern('%fn-put-%in')
        
        self.do = DirectObject()
        self.do.accept('vistrace-into-p_bike', visIn)
        self.do.accept('aimtrace-into-p_bike', visOut)
		
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
          