#generic bike class

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
from panda3d.core import *
from panda3d.physics import *
import sys, math, random

from Bullet import *

class Bike(DirectObject):
    def __init__(self, cTrav):
        self.lights = True
        self.cTrav = cTrav
    
        #load the bike actor and parent it to a physics node
        self.physNode = NodePath("PhysicsNode")
        self.physNode.reparentTo(render)
        self.actNode = ActorNode("bike-phys")
        self.actNodePath = self.physNode.attachNewNode(self.actNode)
        #base.physicsMgr.attachPhysicalNode(actNode)
        
        #create empty list for bullets and a task for updating the positions
        self.bulletList = []
        self.bullet = Bullet(self.cTrav)
        taskMgr.add(self.bullet.update, "bulletTask")
    
        
        #load the bike actor and parent it to a physics node
        #self.bike = Actor("temp_bike.egg", {"move":"bike-move", "shoot":"bike-shoot"})
        self.bike = Actor("motorcycle1.egg", {"move":"bike-move", "shoot":"bike-shoot"})
        self.bike.reparentTo(render)
        self.bike.setScale(.5)
        
        #load the gun actors
        self.gun1 = Actor("temp_gun.egg", {"shoot":"gun-shoot"})
        self.gun1.reparentTo(self.bike)
        self.gun1.setPos(-.5, 0, .5)
        self.gun1.setH(180)
        
        self.gun2 = Actor("temp_gun.egg", {"shoot":"gun-shoot"})
        self.gun2.reparentTo(self.bike)
        self.gun2.setPos(.46, 0, 1)
        self.gun2.setH(180)
        self.gun2.setR(180)
        
        #load the headlight models
        self.headlight1 = loader.loadModel("temp_light.egg")
        self.headlight1.reparentTo(self.bike)
        self.headlight1.setPos(.3, .55, .4)
        self.headlight1.setScale(.75)
        
        #load the headlight models
        self.headlight2 = loader.loadModel("temp_light.egg")
        self.headlight2.reparentTo(self.bike)
        self.headlight2.setPos(-.3, .55, .4)
        self.headlight2.setScale(.75)
        
        #setup a move task for the bike
        #taskMgr.add(self.move, "moveTask")
        self.prevTime = 0
        self.isMoving = False
        
        #setup a shoot task for the bike
        #taskMgr.add(self.shoot, "shootTask")
        self.shotClock = 25
        # for shooting anim self.isShooting = False
        
        #setup a moving dictionary
        #self.moveMap = {"left":0, "right":0, "forward":0}
        
        
        ###
        
        #pusher collision spheres
        #front
        collisionPusher = CollisionHandlerPusher()
        collisionPusher.setInPattern("e_bike-%in")
        cPushSphere = CollisionSphere((0,3.5,2),2)
        
        cNode1 = CollisionNode("e_bike_push")
        cNode1.addSolid(cPushSphere)
        cNode1.setIntoCollideMask(0x10)
        cNode1.setFromCollideMask(0x0)
        self.cNodePath1 = self.bike.attachNewNode(cNode1)
        
        #self.cNodePath1.show()
        
        collisionPusher.addCollider(self.cNodePath1, self.bike)
        self.cTrav.addCollider(self.cNodePath1, collisionPusher)
        
        #middle
        cPushSphere = CollisionSphere((0,0,2),2)
        
        cNode2 = CollisionNode("e_bike_push")
        cNode2.addSolid(cPushSphere)
        cNode2.setIntoCollideMask(0x10)
        cNode2.setFromCollideMask(0x0)
        self.cNodePath2 = self.bike.attachNewNode(cNode2)
        
        #self.cNodePath2.show()
        
        collisionPusher.addCollider(self.cNodePath2, self.bike)
        self.cTrav.addCollider(self.cNodePath2, collisionPusher)
        
        #back
        cPushSphere = CollisionSphere((0,-2.5,2),2)
        
        cNode3 = CollisionNode("e_bike_push")
        cNode3.addSolid(cPushSphere)
        cNode3.setIntoCollideMask(0x10)
        cNode3.setFromCollideMask(0x0)
        self.cNodePath3 = self.bike.attachNewNode(cNode3)
        
        #self.cNodePath3.show()
        
        collisionPusher.addCollider(self.cNodePath3, self.bike)
        self.cTrav.addCollider(self.cNodePath3, collisionPusher)
        
        ###
        
        #cHandler = CollisionHandlerEvent()
        #cHandler.setInPattern("e_bike-%in")
        cSphere = CollisionSphere((0, 0, .75), 1)
        cNode = CollisionNode("e_bike")
        cNode.addSolid(cSphere)
        #cNode.setIntoCollideMask(BitMask32.allOff())
        cNode.setIntoCollideMask(BitMask32(0x10)) # Player bike collides into enemy bike
        cNode.setFromCollideMask(BitMask32.allOff())
        self.cNodePath = self.bike.attachNewNode(cNode)
        self.cNodePath.show()
        #self.cTrav.addCollider(self.cNodePath, cHandler)
        
        #setup the node as a pusher
        pusher = CollisionHandlerPusher()
        pusher.addCollider(self.cNodePath, self.bike)
        
        #show the node
        #self.cNodePath.show()
        
        #add the collider to the traverser
        base.cTrav.addCollider(self.cNodePath, pusher)
        
        #setup and parent spotlights to the player
        self.spotlight1 = Spotlight("headlight1")
        self.spotlight1.setColor((1, 1, 1, 1))
        lens = PerspectiveLens()
        #can change size of cone
        lens.setFov(20)
        self.spotlight1.setLens(lens)
        self.spotlight1.setExponent(100)
        self.spotnode1 = self.headlight1.attachNewNode(self.spotlight1)
        render.setLight(self.spotnode1)
        
        """
        self.spotlight2 = Spotlight("headlight2")
        self.spotlight2.setColor((1, 1, 1, 1))
        self.spotlight2.setLens(lens)
        self.spotlight2.setExponent(100)
        self.spotnode2 = self.headlight2.attachNewNode(self.spotlight2)
        render.setLight(self.spotnode2)"""
        
    """
    def setDirection(self, key, value):
        #set the direction as on or off
        self.moveMap[key] = value
    """
        
    def setShoot(self, value):
        
        self.shootCheck = value
        print("set shoot =", self.shootCheck)
    
    def shoot(self):
        if self.shotClock >= 25:
            #create a bullet
            self.bullet.createBullet(self.gun1, self.bike)
            self.shotClock = 0
        else:
            self.shotClock += 1
        
    """
    def move(self, task):
        elapsed = task.time - self.prevTime
        
        #check key map
        if self.moveMap['left']:
            self.bike.setH(self.bike.getH() + elapsed * 100)
        if self.moveMap['right']:
            self.bike.setH(self.bike.getH() - elapsed * 100)
        if self.moveMap['forward']:
            dist = 8 * elapsed
            angle = deg2Rad(self.bike.getH())
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            self.bike.setPos(self.bike.getX() - dx, self.bike.getY() - dy, 0)
        
        if self.moveMap['left'] or self.moveMap['right'] or self.moveMap['forward']:
            if self.isMoving == False:
                self.isMoving = True
                #self.bike.loop("walk")
        else:
            if self.isMoving:
                self.isMoving = False
                self.bike.stop()
                #self.bike.pose("walk", 4)
        
        self.prevTime = task.time
        return Task.cont
    """
        
    def setupCollisions(self):
        pass
        
    def lightsToggle(self):
        if self.lights:
            self.lightsOff()
        else:
            self.lightsOn()
        
    def lightsOff(self):
        self.lights = False
        render.clearLight(self.spotnode1)
        
    def lightsOn(self):
        self.lights = True
        render.setLight(self.spotnode1)
        