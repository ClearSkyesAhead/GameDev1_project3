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

        #set up inner box point lights
        """
        plight1 = PointLight('plight1')
        plight1.setColor(VBase4(1,1,1,1))
        plight1.setAttenuation(Point3(0,0,.01))
        plnp1 = render.attachNewNode(plight1)
        plnp1.setPos(-20.5,16.5,13.5)
        render.setLight(plnp1)
        
        plight2 = PointLight('plight1')
        plight2.setColor(VBase4(1,1,1,1))
        plight2.setAttenuation(Point3(0,0,.01))
        plnp2 = render.attachNewNode(plight2)
        plnp2.setPos(20.5,16.5,13.5)
        render.setLight(plnp2)
        
        plight3 = PointLight('plight1')
        plight3.setColor(VBase4(1,1,1,1))
        plight3.setAttenuation(Point3(0,0,.01))
        plnp3 = render.attachNewNode(plight3)
        plnp3.setPos(20.5,-16.5,13.5)
        render.setLight(plnp3)
        
        plight4 = PointLight('plight1')
        plight4.setColor(VBase4(1,1,1,1))
        plight4.setAttenuation(Point3(0,0,.01))
        plnp4 = render.attachNewNode(plight4)
        plnp4.setPos(-20.5,-16.5,13.5)
        render.setLight(plnp4)"""
        
        """temp_ball = loader.loadModel('temp_bullet')
        temp_ball.setScale(2)
        temp_ball.setPos(-20.5,16.5,13.5)
        temp_ball.reparentTo(render)
        
        cSphere = CollisionSphere((0,0,0),.5)
        
        cNode = CollisionNode("p_bike_push")
        cNode.addSolid(cSphere)
        cNodePath = temp_ball.attachNewNode(cNode)
        cNodePath.show()"""
