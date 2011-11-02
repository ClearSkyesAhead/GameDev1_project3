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
        #load the terrain model and make it a physics body
        """physNode = NodePath("PhysicsNode")
        physNode.reparentTo(render)
        actNode = ActorNode("terrain-phys")
        actNodePath = physNode.attachNewNode(actNode)
        base.physicsMgr.attachPhysicalNode(actNode)"""
        self.terrain = loader.loadModel("temp_terrain.egg")
        #self.terrain.reparentTo(actNodePath)
        self.terrain.reparentTo(render)
        
        #set a collide mask
        #self.terrain.setCollideMask(BitMask32.allOff())
        #self.terrain.setCollideMask(BitMask32.bit(0))
        self.terrain.setCollideMask(1)