#player bike class

#importing all the panda stuff since I'm not sure which ones i need

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random

class PlayerBike(DirectObject):
    def __init__(self):
        #load the bike actor
        self.bike = Actor("temp_bike.egg", {"move":"bike-move", "shoot":"bike-shoot"})
        self.bike.reparentTo(render)
        
        #setup a move task for the bike
        taskMgr.add(self.move, "moveTask")
        self.prevTime = 0
        self.isMoving = False
        
        #setup a moving dictionary
        self.moveMap = {"left":0, "right":0, "forward":0}
        
        
        #setup collision sphere
        base.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerEvent()
        
        cSphere = CollisionSphere((0,0,.75), .75)
        cNode = CollisionNode("p_bike")
        cNode.addSolid(cSphere)
        cNodePath = self.bike.attachNewNode(cNode)
        
        #setup the node as a pusher
        pusher = CollisionHandlerPusher()
        pusher.addCollider(cNodePath, self.bike)
        
        #show the node
        cNodePath.show()
        
        #add the collider to the traverser
        base.cTrav.addCollider(cNodePath, pusher)
        
    def setDirection(self, key, value):
        #set the direction as on or off
        self.moveMap[key] = value
        
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
        
    def setupCollisions(self):
        pass
        
        