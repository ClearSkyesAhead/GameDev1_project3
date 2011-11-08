#terrain class

#importing all the panda stuff since I'm not sure which ones i need

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random

class Terrain(DirectObject):
    def __init__(self):
        #load the terrain model
        #self.terrain = loader.loadModel("temp_terrain.egg")
        #self.terrain = loader.loadModel("test_terrain_jump.egg")
        self.terrain = loader.loadModel("terrain.egg")

        #self.terrain.reparentTo(actNodePath)
        self.terrain.reparentTo(render)
        self.terrain.setScale(.85)
        
        #set a collide mask
        #self.terrain.setCollideMask(BitMask32.allOff())
        #self.terrain.setCollideMask(BitMask32.bit(0))
        self.terrain.setCollideMask(2)
        
        taskMgr.add(self.powerUpUpdate, "powerUpTask")
        
        #setup power up collision spheres
        #powerup1 collision sphere (invincibility)
        cPowerSphere1 = CollisionSphere((0,-.3,16.5),3)
        cPowerNode1 = CollisionNode("powerup1")
        cPowerNode1.addSolid(cPowerSphere1)
        cPowerNode1.setIntoCollideMask(1)
        self.cPowerNode1Path = render.attachNewNode(cPowerNode1)
        self.cPowerNode1Path.show()
        self.powerUp1 = True
        self.powerUp1Count = 0
        
        #powerup2 collision sphere (matched with powerup3)
        cPowerSphere2 = CollisionSphere((.5,77,18.5),3)
        cPowerNode2 = CollisionNode("powerup2")
        cPowerNode2.addSolid(cPowerSphere2)
        cPowerNode2.setIntoCollideMask(1)
        self.cPowerNode2Path = render.attachNewNode(cPowerNode2)
        self.cPowerNode2Path.show()
        self.powerUp2 = True
        self.powerUp2Count = 0
        
        #powerup3 collision sphere (matched with powerup2)
        cPowerSphere3 = CollisionSphere((.5,-77,18.5),3)
        cPowerNode3 = CollisionNode("powerup3")
        cPowerNode3.addSolid(cPowerSphere3)
        cPowerNode3.setIntoCollideMask(1)
        self.cPowerNode3Path = render.attachNewNode(cPowerNode3)
        self.cPowerNode3Path.show()
        self.powerUp3 = True
        self.powerUp3Count = 0
        
        #powerup4 collision sphere (matched with powerup4)
        cPowerSphere4 = CollisionSphere((77,-1,18.5),3)
        cPowerNode4 = CollisionNode("powerup4")
        cPowerNode4.addSolid(cPowerSphere4)
        cPowerNode4.setIntoCollideMask(1)
        self.cPowerNode4Path = render.attachNewNode(cPowerNode4)
        self.cPowerNode4Path.show()
        self.powerUp4 = True
        self.powerUp4Count = 0
        
        #powerup5 collision sphere (matched with powerup5)
        cPowerSphere5 = CollisionSphere((-77,-1,18.5),3)
        cPowerNode5 = CollisionNode("powerup5")
        cPowerNode5.addSolid(cPowerSphere5)
        cPowerNode5.setIntoCollideMask(1)
        self.cPowerNode5Path = render.attachNewNode(cPowerNode5)
        self.cPowerNode5Path.show()
        self.powerUp5 = True
        self.powerUp5Count = 0
        
        #setup lights for outer box
        plight5 = PointLight('plight1')
        plight5.setColor(VBase4(1,1,1,1))
        plight5.setAttenuation(Point3(0,0,.01))
        plnp5 = render.attachNewNode(plight5)
        plnp5.setPos(-37.5,39.5,13.5)
        render.setLight(plnp5)
        
        plight6 = PointLight('plight1')
        plight6.setColor(VBase4(1,1,1,1))
        plight6.setAttenuation(Point3(0,0,.01))
        plnp6 = render.attachNewNode(plight6)
        plnp6.setPos(37.5,39.5,13.5)
        render.setLight(plnp6)
        
        plight7 = PointLight('plight1')
        plight7.setColor(VBase4(1,1,1,1))
        plight7.setAttenuation(Point3(0,0,.01))
        plnp7 = render.attachNewNode(plight7)
        plnp7.setPos(37.5,-39.5,13.5)
        render.setLight(plnp7)
        
        plight8 = PointLight('plight1')
        plight8.setColor(VBase4(1,1,1,1))
        plight8.setAttenuation(Point3(0,0,.01))
        plnp8 = render.attachNewNode(plight8)
        plnp8.setPos(-37.5,-39.5,13.5)
        render.setLight(plnp8)

    def powerUpUpdate(self, task):
        #check powerup1
        if self.powerUp1 == False:
            #print('increasing count')
            self.powerUp1Count += 1
        if self.powerUp1Count == 50:
            #print('making a new one')
            self.powerUp1 = True
            self.powerUp1Count = 0
            cPowerSphere1 = CollisionSphere((0,-.3,16.5),3)
            cPowerNode1 = CollisionNode("powerup1")
            cPowerNode1.addSolid(cPowerSphere1)
            cPowerNode1.setIntoCollideMask(1)
            self.cPowerNode1Path = render.attachNewNode(cPowerNode1)
            self.cPowerNode1Path.show()
        
        #check powerup2
        if self.powerUp2 == False:
            #print('increasing count')
            self.powerUp2Count += 1
        if self.powerUp2Count == 50:
            #print('making a new one')
            self.powerUp2 = True
            self.powerUp2Count = 0
            cPowerSphere2 = CollisionSphere((.5,77,18.5),3)
            cPowerNode2 = CollisionNode("powerup2")
            cPowerNode2.addSolid(cPowerSphere2)
            cPowerNode2.setIntoCollideMask(1)
            self.cPowerNode2Path = render.attachNewNode(cPowerNode2)
            self.cPowerNode2Path.show()
            
        #check powerup3
        if self.powerUp3 == False:
            #print('increasing count')
            self.powerUp3Count += 1
        if self.powerUp3Count == 50:
            #print('making a new one')
            self.powerUp3 = True
            self.powerUp3Count = 0
            cPowerSphere3 = CollisionSphere((.5,-77,18.5),3)
            cPowerNode3 = CollisionNode("powerup3")
            cPowerNode3.addSolid(cPowerSphere3)
            cPowerNode3.setIntoCollideMask(1)
            self.cPowerNode3Path = render.attachNewNode(cPowerNode3)
            self.cPowerNode3Path.show()
            
        #check powerup4
        if self.powerUp4 == False:
            #print('increasing count')
            self.powerUp4Count += 1
        if self.powerUp4Count == 50:
            #print('making a new one')
            self.powerUp4 = True
            self.powerUp4Count = 0
            cPowerSphere4 = CollisionSphere((77,-1,18.5),3)
            cPowerNode4 = CollisionNode("powerup4")
            cPowerNode4.addSolid(cPowerSphere4)
            cPowerNode4.setIntoCollideMask(1)
            self.cPowerNode4Path = render.attachNewNode(cPowerNode4)
            self.cPowerNode4Path.show()
            
        #check powerup5
        if self.powerUp5 == False:
            #print('increasing count')
            self.powerUp5Count += 1
        if self.powerUp5Count == 50:
            #print('making a new one')
            self.powerUp5 = True
            self.powerUp5Count = 0
            cPowerSphere5 = CollisionSphere((-77,-1,18.5),3)
            cPowerNode5 = CollisionNode("powerup5")
            cPowerNode5.addSolid(cPowerSphere5)
            cPowerNode5.setIntoCollideMask(1)
            self.cPowerNode5Path = render.attachNewNode(cPowerNode5)
            self.cPowerNode5Path.show()
        return Task.cont
