#main function

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
from direct.gui.OnscreenImage import OnscreenImage
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
        base.camera.reparentTo(self.p_bike.bike)
        base.camera.setZ(6)
        base.camera.setP(-8)
        base.camera.setY(-32)
        
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
        
        #2d attempt
        #will need the health bars as egg or bam file then reparent to render2d
        dr = base.win.makeDisplayRegion()
        dr.setSort(20)

        """myCamera2d = NodePath(Camera('myCam2d'))
        lens = OrthographicLens()
        lens.setFilmSize(2, 2)
        lens.setNearFar(-1000, 1000)
        myCamera2d.node().setLens(lens)

        myRender2d = NodePath('myRender2d')
        myRender2d.setDepthTest(False)
        myRender2d.setDepthWrite(False)
        myCamera2d.reparentTo(myRender2d)
        dr.setCamera(myCamera2d)"""
        
        myImage = OnscreenImage(image = 'map.jpg')
        #myImage.reparentTo(myRender2d)
        myImage.setScale(0.25)
        myImage.setX(1)
        myImage.setZ(1)
        
        
        #self.initAI()
        #self.e_bikes = [self.addEnemy()]
        #self.e_bikes[0].AIbehaviors.pursue(self.p_bike.bike, 0.7)
        #base.cTrav.addCollider(self.p_bike.cNodePath, self.e_bikes[0].cevent)
                
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
        #cycle through the enemy bullets
        for enemy in self.e_bikes:
            for i in range(len(enemy.bullet.bulletList)):
                if cEntry.getIntoNodePath().getParent() == enemy.bullet.bulletList[i]:
                    print('erased')
                    enemy.bullet.bulletTime.remove(enemy.bullet.bulletTime[i])
                    enemy.p_bike.bullet.bulletList.remove(enemy.bullet.bulletList[i])
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
