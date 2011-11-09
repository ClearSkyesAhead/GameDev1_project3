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
        self.start = False
        self.mainScreen = OnscreenImage(image = 'mainScreen.png')
        #self.mainScreen.setScale(1.25)
        self.accept("mouse1", self.begin)
    def begin(self):
        self.start = True
        self.mainScreen.destroy()
        self.__init__1()
    def __init__1(self):
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
        
        self.dead = False
        self.deadCount = 0
        taskMgr.add(self.gameOverDead, 'deadTask')
        
        self.win = False
        self.winCount = 0
        taskMgr.add(self.gameOverWin, 'winTask')
        
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
        
        self.playerHealth = OnscreenImage(image = 'PlayerHealthBar.png')
        self.playerHealth.setX(-1)
        self.playerHealth.setZ(-1.95)
        
        #enemy health
        self.enemyHealth = OnscreenImage(image = 'EnemyHealthBar.png')
        self.enemyHealth.setX(1)
        self.enemyHealth.setZ(-1.95)
        
        
        #self.initAI()
        #self.e_bikes = [self.addEnemy()]
        #base.cTrav.addCollider(self.p_bike.cNodePath1, self.e_bikes[0].cevent)
        
    def gameOverDead(self, task):
        if self.dead == True:
            self.deadCount += 1
        if self.deadCount > 200:
            self.gameOver = OnscreenImage(image = 'gameOver.png')
            self.gameOver.setScale(1.35)
        return Task.cont
        
    def gameOverWin(self, task):
        if self.win == True:
            self.winCount += 1
        if self.winCount > 200:
            self.gameOverWin = OnscreenImage(image = 'win.png')
            self.gameOverWin.setScale(1.35)
        return Task.cont
        
    def powerupCollision(self, cEntry):
        #check powerup1
        if cEntry.getIntoNodePath() == self.w_terrain.cPowerNode1Path:
            self.w_terrain.powerUp1 = False
            self.p_bike.invin = True
            #print('I WIN')
        #check powerup2
        elif cEntry.getIntoNodePath() == self.w_terrain.cPowerNode2Path:
            self.w_terrain.powerUp2 = False
            self.p_bike.shotgun = True
            self.p_bike.p_up_timer = 0
        #check powerup3
        elif cEntry.getIntoNodePath() == self.w_terrain.cPowerNode3Path:
            self.w_terrain.powerUp3 = False
            self.p_bike.shotgun = True
            self.p_bike.p_up_timer = 0
        #check power4
        elif cEntry.getIntoNodePath() == self.w_terrain.cPowerNode4Path:
            self.w_terrain.powerUp4 = False
            self.p_bike.health_up = True
        #check powerup5
        elif cEntry.getIntoNodePath() == self.w_terrain.cPowerNode5Path:
            self.w_terrain.powerUp5 = False
            self.p_bike.health_up = True
        cEntry.getIntoNodePath().remove()
        
    def bulletCollision(self, cEntry):
        #check which bike is being hit
        if self.p_bike.invin == False and (cEntry.getFromNodePath() == self.p_bike.cNodePath1 or cEntry.getFromNodePath() == self.p_bike.cNodePath1 or cEntry.getFromNodePath() == self.p_bike.cNodePath3):
            print('player bike!')
            self.p_bike.hp -= 1
            self.playerHealth.getX() - .1
            if self.p_bike.hp <= 0:
                #kill player bike and reset camera
                taskMgr.remove("moveTask")
                taskMgr.remove("bulletTask")
                taskMgr.remove("shootTask")
                taskMgr.remove("powerupTask")
                x = base.camera.getX() + self.p_bike.bike.getX()
                y = base.camera.getY() + self.p_bike.bike.getY()
                h = self.p_bike.bike.getH()
                
                angle = deg2Rad(self.p_bike.bike.getH())
                dy = -math.cos(angle)
                dx = math.sin(angle)
                
                dx = -dx * 32
                dy = -dy * 32
                
                base.camera.reparentTo(render)
                base.camera.setPos(0,0,0)
                base.camera.setPosHpr( self.p_bike.bike.getX() - dx, self.p_bike.bike.getY() - dy, 7, self.p_bike.bike.getH(), -8, 0)
                
                
                
                x = self.p_bike.bike.getX()
                y = self.p_bike.bike.getY()
                z = self.p_bike.bike.getZ()
                h = self.p_bike.bike.getH()
                
                self.p_bike.bike.delete()
                self.death_player = Actor("moto2_deadActor.egg", {"death":"moto2_deadAnim.egg"})
                self.death_player.reparentTo(render)
                self.death_player.setPos(x,y,z)
                self.death_player.setH(h)
                self.animcontrol = self.death_player.getAnimControl('death')
                self.death_player.play("death")
                self.dead = True
        
        #UNCOMMENT WHEN ENEMY BIKES ARE FIXED
        """else:
            for enemy in self.e_bikes:
                if cEntry.getFromNodePath() == enemy.cNodePath:
                    enemy.hp -= 1
                    self.enemyHealth.getX() + .1
                    if enemy.hp <= 0:
                        print('Game Over. You Win!')
                        #kill enemy bike
                        enemy.delete()
                        self.death_enemy = Actor("moto1_deadActor.egg", {"death":"moto1_deadAnim.egg"})
                        self.death_enemy.reparentTo(render)
                        self.death_enemy.setPos(x,y,z)
                        self.death_enemy.setH(h)
                        self.death_enemy.play("death")
                        self.win = True
                    break"""
        #destroy the bullet
        for i in range(len(self.p_bike.bullet.bulletList)):
            if cEntry.getIntoNodePath().getParent() == self.p_bike.bullet.bulletList[i]:
                print('erased')
                self.p_bike.bullet.bulletTime.remove(self.p_bike.bullet.bulletTime[i])
                self.p_bike.bullet.bulletList.remove(self.p_bike.bullet.bulletList[i])
                cEntry.getIntoNodePath().getParent().remove()
                break
        #UNCOMMENT WHEN ENEMY BIKES ARE FIXED
        """#cycle through the enemy bullets
        for enemy in self.e_bikes:
            for i in range(len(enemy.bullet.bulletList)):
                if cEntry.getIntoNodePath().getParent() == enemy.bullet.bulletList[i]:
                    print('erased')
                    enemy.bullet.bulletTime.remove(enemy.bullet.bulletTime[i])
                    enemy.bullet.bulletList.remove(enemy.bullet.bulletList[i])
                    cEntry.getIntoNodePath().getParent().remove()
                    break"""
        
    def initAI(self):
        self.AIworld = AIWorld(render)
        #self.AIworld.addObstacle(self.w_terrain.wall_terrain)
        self.AIworld.addObstacle(self.w_terrain.cNodePathWall1)
        self.AIworld.addObstacle(self.w_terrain.cNodePathWall2)
        self.AIworld.addObstacle(self.w_terrain.cNodePathWall3)
        self.AIworld.addObstacle(self.w_terrain.cNodePathWall4)
        #AI World update        
        taskMgr.add(self.AIUpdate,"AIUpdate")
    
    def AIUpdate(self, task):
        self.AIworld.update()
        for i in self.e_bikes:
            i.update()
            i.bike.setHpr(i.bike.getH(), 0, i.bike.getR())
            i.bike.setY(max(0.0, i.bike.getY()))
        return Task.cont
        
    def addEnemy(self):
        enemy = EnemyBike(base.cTrav, self.cevent)
        enemy.target = self.p_bike
        enemy.setMode('scan')
        self.AIworld.addAiChar(enemy.AIchar)
        base.cTrav.addCollider(self.p_bike.cNodePath1, enemy.cevent)
        
        return enemy



w = World()
run()
