#main function

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random

class World(DirectObject):
    def __init__(self):
        camera.setPosHpr(0, -15, 7, 0, -15, 0)
        #load all the models
        self.loadModels()
    
    def loadModels(self):
        """loads initial models into the world"""
        
        #directly load the terrain and bike
        self.bike = loader.loadModel("temp_bike.egg")
        self.bike.reparentTo(render)
        #self.bike.setScale(.005)
        
        self.terrain = loader.loadModel("temp_terrain.egg")
        self.terrain.reparentTo(render)
        
w = World()
run()
