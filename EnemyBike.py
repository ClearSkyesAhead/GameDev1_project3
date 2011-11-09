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
        self.bike.setPos(10, 0, 0)
        self.initAI()
        self.hp = 10
        
        self.singleShot = base.loader.loadSfx('50Cal.mp3')
        
        self.shooting = 0
        self.decshooting = True
        self.targeting = 0
        self.dectargeting = True
        
        frombikemask = BitMask32(0x10)
        intobikemask = BitMask32.allOff()
        floormask = BitMask32(0x2)
        
        self.cevent = CollisionHandlerEvent()
        self.cevent.addInPattern('%fn-into-%in')
        self.cevent.addOutPattern('%fn-out-%in')
        
        self.bullettrace = self.bike.attachNewNode(CollisionNode('aimtrace'))
        self.bullettrace.node().addSolid(CollisionRay(0, 0, 0, 0, -1, .1))
        self.bullettrace.node().setFromCollideMask(frombikemask)
        self.bullettrace.node().setIntoCollideMask(intobikemask)
        #self.bullettrace.show()
        #base.cTrav.addCollider(self.bullettrace, self.bike)
        base.cTrav.addCollider(self.bullettrace, self.cevent)
        
        self.gravtrace = self.bike.attachNewNode(CollisionNode('colNode'))
        self.gravtrace.node().addSolid(CollisionRay(0, 0, 0, 0, 0, -1))
        self.gravtrace.node().setFromCollideMask(floormask)
        self.gravtrace.node().setIntoCollideMask(BitMask32.allOff())
        #self.gravtrace.show()
        
        self.vistrace = self.bike.attachNewNode(CollisionNode('vistrace'))
        self.vistrace.node().addSolid(CollisionRay(0, 0, 0, 0, -1, .15))
        #self.vistrace.node().addSolid(CollisionRay(0, 0, 0, 1, 1, 0))
        #self.vistrace.node().addSolid(CollisionRay(0, 0, 0, -1, 1, 0))
        self.vistrace.node().addSolid(CollisionRay(0, 0, 0, 1, -1, .15))
        self.vistrace.node().addSolid(CollisionRay(0, 0, 0, -1, -1, .15))
        self.vistrace.node().setFromCollideMask(frombikemask)
        self.vistrace.node().setIntoCollideMask(intobikemask)
        #self.vistrace.show()
        #base.cTrav.addCollider(self.vistrace, self.bike)
        base.cTrav.addCollider(self.vistrace, self.cevent)
         
        self.lifter = CollisionHandlerFloor()
        self.lifter.setMaxVelocity(9.8)
        base.cTrav.addCollider(self.gravtrace,self.lifter)
        self.lifter.addCollider(self.gravtrace, self.bike)
        
        
        
        
        self.do = DirectObject()
        self.do.accept('vistrace-into-p_bike_push', self.visIn)
        self.do.accept('vistrace-out-p_bike_push', self.visOut)
        self.do.accept('aimtrace-into-p_bike_push', self.aimIn)
        self.do.accept('aimtrace-out-p_bike_push', self.aimOut)
        
        self.prev = self.bike.getPos()
		
    def initAI(self):
        self.AIchar = AICharacter("Enemy Bike", self.bike, 100, 0.05, 100)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        
        self.AImode = 'scan'
        self.target = None
        
        """
        l = loader.loadModel("shield.egg")
        l.reparentTo(render)
        l.setPos(70.0, 70.0, 0.0)
        l = loader.loadModel("shield.egg")
        l.reparentTo(render)
        l.setPos(70.0, -70.0, 0.0)
        l = loader.loadModel("shield.egg")
        l.reparentTo(render)
        l.setPos(-70.0, 70.0, 0.0)
        l = loader.loadModel("shield.egg")
        l.reparentTo(render)
        l.setPos(-70.0, -70.0, 0.0)
        """
		
    def update(self):
        #self.shoot()
        if self.AImode == 'flee':
            if random.randint(1, 60) == 1:
                self.lightsToggle()
        
        if (self.bike.getPos() - self.prev).length() > 0.01:
            self.bike.loop("move")
        else:
            #self.bike.stop()
            pass
        self.prev = self.bike.getPos()
        
        if self.shooting > 0:
            self.shoot()
            if self.decshooting:
                self.shooting -= 1
        if self.targeting > 0:
            if self.dectargeting:
                self.targeting -= 1
                if self.targeting == 0:
                    self.setMode('scan')
        if self.hp <= 1:
            self.setMode('flee')
        
        #print "shooting: " + str(self.shooting) + " (" + str(self.decshooting) + ")"
        #print "targeting: " + str(self.targeting) + " (" + str(self.dectargeting) + ")"
            
    def shoot(self):
        
        if self.shotClock >= 25:
            #create a bullet
            self.singleShot.play()
            #this may be the worst thing ever
            self.bike.setH((self.bike.getH() - 180.0) % 360.0)
            self.bullet.createBullet(self.bike)
            self.bike.setH((self.bike.getH() + 180.0) % 360.0)
            self.shotClock = 0
        else:
            self.shotClock += 1
            
            
    def setMode(self, mode):
        self.AImode = mode
        #self.AIbehaviors.removeAi("all")
        
        mag = 70.0
        r1 = 10.0
        r2 = 2.0
        #self.AIbehaviors.flee(Vec3(mag, mag, 0.0), r1, r2, 1.0)
        #self.AIbehaviors.flee(Vec3(mag, -mag, 0.0), r1, r2, 1.0)
        #self.AIbehaviors.flee(Vec3(-mag, mag, 0.0), r1, r2, 1.0)
        #self.AIbehaviors.flee(Vec3(-mag, -mag, 0.0), r1, r2, 1.0)
        #print self.AImode
        if self.AImode == 'target':
            #self.AIchar.setMaxForce(100);
            self.AIbehaviors.wander(0.5, 0, 17, 0.25)
            self.AIbehaviors.pursue(self.target.dummy, 0.5)
            self.AIbehaviors.evade(self.target.dummy, 4.0, 2.5, 0.95)
            
        elif self.AImode == 'flee':
            #self.AIchar.setMaxForce(100);
            self.AIbehaviors.wander(1.0, 0, 17, 0.5)
            self.AIbehaviors.pursue(self.target.dummy, 0.0)
            self.AIbehaviors.evade(self.target.dummy, 3.0, 6.0, 1.0)
        elif self.AImode == 'scan':
            #self.AIchar.setMaxForce(100);
            self.AIbehaviors.wander(0.5, 0, 17, 0.35)
            self.AIbehaviors.pursue(self.target.dummy, 0.5)
            self.AIbehaviors.evade(self.target.dummy, 3.0, 2.5, 0.85)
        
        
            
            
    def aimIn(self, event):
        #print length(self.bike.getPos(), event.getFromNodePath().getPos())
        #self.AImode = 'target'
        #print event.getFromNodePath().getParent().AImode
        #print event
        self.shooting = 60
        self.decshoot = False
        
    def aimOut(self, event):
        #print event
        self.decshoot = True

    def visIn(self, event):
        #print self.physNode.getPos()
        #print (self.bike.getPos() - event.getIntoNodePath().getPos()).length()
        self.setMode('target')
        self.targeting = 5
        self.dectargeting = False

        
    def visOut(self, event):
        self.dectargeting = True