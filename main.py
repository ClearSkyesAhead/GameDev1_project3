#main function

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
from panda3d.ai import *
from panda3d.core import *
from panda3d.physics import *
import sys, math, random

#our modules
from PlayerBike import PlayerBike
from Terrain import Terrain
from EnemyBike import EnemyBike

class World(DirectObject):
    def __init__(self):
        #load physics
        base.enableParticles()
        
        #create a traverser
        base.cTrav = CollisionTraverser()
        
        self.cevent = CollisionHandlerEvent()
        
        self.cevent.addInPattern('into-%in')
        self.cevent.addOutPattern('outof-%in')
        
        #load all the models
        self.w_terrain = Terrain()
        self.p_bike = PlayerBike(base.cTrav)
        
        #disable mouse
        base.disableMouse()
        
        #load and play background sound
        backgroundSound = base.loader.loadSfx('Modern_Battlefield.mp3')
        backgroundSound.setLoop(True)
        backgroundSound.play()
        
        #parent the camera to the player bike and offset the initial location
        camera.reparentTo(self.p_bike.bike)
        camera.setZ(8)
        camera.setP(-9)
        camera.setY(-30)
        
        #set up accept tasks
        #close the game
        self.accept("escape", sys.exit)
        
        #handle movement
        self.accept("arrow_up", self.p_bike.setDirection, ["forward", 1])
        self.accept("arrow_right", self.p_bike.setDirection, ["right", 1])
        self.accept("arrow_left", self.p_bike.setDirection, ["left", 1])
        self.accept("arrow_up-up", self.p_bike.setDirection, ["forward", 0])
        self.accept("arrow_right-up", self.p_bike.setDirection, ["right", 0])
        self.accept("arrow_left-up", self.p_bike.setDirection, ["left", 0])
        
        #handle shooting
        self.accept("space", self.p_bike.setShoot, [1])
        self.accept("space-up", self.p_bike.setShoot, [0])
        
        #powerup collisions
        self.accept("p_bike-powerup1", self.powerupCollision)
        self.accept("p_bike-powerup2", self.powerupCollision)
        self.accept("p_bike-powerup3", self.powerupCollision)
        self.accept("p_bike-powerup4", self.powerupCollision)
        self.accept("p_bike-powerup5", self.powerupCollision)
        
        #bullet collision with player
        self.accept("p_bike-bullet", self.bulletCollision)
        self.accept("e_bike-bullet", self.bulletCollision)
        
        #setup basic environment lighting
        self.ambientLight = AmbientLight("ambientLight")
        self.ambientLight.setColor((.25, .25, .25, 1))
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        render.setLight(self.ambientLightNP)
        render.setShaderAuto()
        
        """self.initAI()
        self.e_bikes = [self.addEnemy()]
        #self.e_bikes[0].AIbehaviors.pursue(self.p_bike.bike, 0.7)"""
    
    def testCollision(self, cEntry):
        #check if in collision
        print("test")
        #remove test sphere
        cEntry.getIntoNodePath().remove()
        #find the right bullet in the list to remove and the right time index
        for i in range(len(self.p_bike.bullet.bulletList)):
            if cEntry.getFromNodePath().getParent() == self.p_bike.bullet.bulletList[i]:
                print('erased')
                self.p_bike.bullet.bulletTime.remove(self.p_bike.bullet.bulletTime[i])
                self.p_bike.bullet.bulletList.remove(self.p_bike.bullet.bulletList[i])
                cEntry.getFromNodePath().getParent().remove()
                break
                
    def powerupCollision(self, cEntry):
        #check which powerup
        #activate it
        #print(cEntry.getIntoNodePath())
        #check powerup1
        if cEntry.getIntoNodePath() == self.w_terrain.cPowerNode1Path:
            self.w_terrain.powerUp1 = False
            #print('I WIN')
        #check powerup2
        elif cEntry.getIntoNodePath() == self.w_terrain.cPowerNode2Path:
            self.w_terrain.powerUp2 = False
        #check powerup3
        elif cEntry.getIntoNodePath() == self.w_terrain.cPowerNode3Path:
            self.w_terrain.powerUp3 = False
        #check power4
        elif cEntry.getIntoNodePath() == self.w_terrain.cPowerNode4Path:
            self.w_terrain.powerUp4 = False
        #check powerup5
        elif cEntry.getIntoNodePath() == self.w_terrain.cPowerNode5Path:
            self.w_terrain.powerUp5 = False
        cEntry.getIntoNodePath().remove()
        
    def bulletCollision(self, cEntry):
        #check which bike is being hit
        if cEntry.getFromNodePath() == self.p_bike.cNodePath:
            print('player bike!')
            self.p_bike.hp -= 1
            if self.p_bike.hp <= 0:
                print('Game Over. You Lose')
                #kill player bike
                #go to end screen
        else:
            for enemy in self.e_bikes:
                if cEntry.getFromNodePath() == enemy.Bike.cNodePath:
                    enemy.hp -= 1
                    if enemy.hp <= 0:
                        print('Game Over. You Win!')
                        #kill enemy bike
                        #go to end screen
                    break
        #destroy the bullet
        for i in range(len(self.p_bike.bullet.bulletList)):
            if cEntry.getIntoNodePath().getParent() == self.p_bike.bullet.bulletList[i]:
                print('erased')
                self.p_bike.bullet.bulletTime.remove(self.p_bike.bullet.bulletTime[i])
                self.p_bike.bullet.bulletList.remove(self.p_bike.bullet.bulletList[i])
                cEntry.getIntoNodePath().getParent().remove()
                break
    """def initAI(self):
        self.AIworld = AIWorld(render)
 
        #AI World update        
        taskMgr.add(self.AIUpdate,"AIUpdate")
    
    def AIUpdate(self, task):
        self.AIworld.update()
        for i in self.e_bikes:
            i.update()
            i.bike.setHpr(i.bike.getH(), 0, i.bike.getR())
        return Task.cont
        
    def addEnemy(self):
        enemy = EnemyBike(base.cTrav, self.cevent)
        self.AIworld.addAiChar(enemy.AIchar)
        return enemy"""
        
w = World()
run()
