#main function

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random

#our modules
from PlayerBike import PlayerBike
from Terrain import Terrain

class World(DirectObject):
    def __init__(self):
        #load all the models
        self.w_terrain = Terrain()
        self.p_bike = PlayerBike()
        
        #disable mouse
        base.disableMouse()
        #parent the camera to the player bike and offset the initial location
        camera.reparentTo(self.p_bike.bike)
        camera.setZ(7)
        camera.setP(-15)
        camera.setY(-15)
        
        #set up accept tasks
        self.accept("escape", sys.exit)
        self.accept("arrow_up", self.p_bike.setDirection, ["forward", 1])
        self.accept("arrow_right", self.p_bike.setDirection, ["right", 1])
        self.accept("arrow_left", self.p_bike.setDirection, ["left", 1])
        self.accept("arrow_up-up", self.p_bike.setDirection, ["forward", 0])
        self.accept("arrow_right-up", self.p_bike.setDirection, ["right", 0])
        self.accept("arrow_left-up", self.p_bike.setDirection, ["left", 0])
        
        
        
        
w = World()
run()
