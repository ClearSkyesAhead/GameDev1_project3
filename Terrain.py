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
        
        #setup power up collision spheres
        #powerup1 collision sphere
        #test sphere
        cPowerSphere1 = CollisionSphere((5,5,5),1)
        cPowerNode1 = CollisionNode("powerup1")
        cPowerNode1.addSolid(cPowerSphere1)
        cPowerNode1.setIntoCollideMask(1)
        self.cPowerNode1Path = render.attachNewNode(cPowerNode1)
        self.cPowerNode1Path.show()
        self.powerUp1 = True
        self.powerUp1Count = 0
        
        taskMgr.add(self.powerUpUpdate, "powerUpTask")
        
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
        if self.powerUp1 == False:
            print('increasing count')
            self.powerUp1Count += 1
        if self.powerUp1Count == 50:
            print('making a new one')
            self.powerUp1 = True
            self.powerUp1Count = 0
            cPowerSphere1 = CollisionSphere((5,5,5),1)
            cPowerNode1 = CollisionNode("powerup1")
            cPowerNode1.addSolid(cPowerSphere1)
            cPowerNode1.setIntoCollideMask(1)
            self.cPowerNode1Path = render.attachNewNode(cPowerNode1)
            self.cPowerNode1Path.show()
        return Task.cont