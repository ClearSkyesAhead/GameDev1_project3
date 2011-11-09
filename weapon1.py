#Weapon of some sort

#Spread shot, toying around with 3 and 5 shot variants
# for 3 shot simply comment out the 

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random

class weapon1(DirectObject):
    def __init__(self, cTrav):

        #create a constant speed and an overall bullet list to contain all bullets
        self.speed = 100
        self.bulletList = []
        self.bulletTime = []
        self.shot = []
        self.prevTime = 0
        self.prevBulletTime = 0
        self.cTrav = cTrav
        self.timer = 0
        taskMgr.add(self.updateTimer, "timerUpdate")
        
        
    def updateTimer(self, task):
        self.timer += task.time
        
    def createBullet(self, bike):
        #load the model and set the pos and H to the bike's
        self.bullet1 = loader.loadModel("bullet.egg")
        self.bullet2 = loader.loadModel("bullet.egg")
        self.bullet3 = loader.loadModel("bullet.egg")
        self.bullet4 = loader.loadModel("bullet.egg")
        self.bullet5 = loader.loadModel("bullet.egg")
        
        
        
        #prevent bullet from spawning inside of player collision sphere
        angle = deg2Rad(bike.getH())
        dy = -math.cos(angle) * 5
        dx = math.sin(angle) * 5
        
        self.bullet1.setPos(bike.getX() - dx, bike.getY() - dy, bike.getZ())
        self.bullet2.setPos(bike.getX() - dx, bike.getY() - dy, bike.getZ())
        self.bullet3.setPos(bike.getX() - dx, bike.getY() - dy, bike.getZ())
        self.bullet4.setPos(bike.getX() - dx, bike.getY() - dy, bike.getZ())
        self.bullet5.setPos(bike.getX() - dx, bike.getY() - dy, bike.getZ())
        
        self.bullet1.setH(bike.getH()+15)
        self.bullet2.setH(bike.getH()-15)
        self.bullet3.setH(bike.getH())
        self.bullet4.setH(bike.getH()+7.5)
        self.bullet5.setH(bike.getH()-7.5)
        
        self.bullet1.setScale(.25)
        self.bullet2.setScale(.25)
        self.bullet3.setScale(.25)
        self.bullet4.setScale(.25)
        self.bullet5.setScale(.25)
        
        self.bullet1.reparentTo(render)
        self.bullet2.reparentTo(render)
        self.bullet3.reparentTo(render)
        self.bullet4.reparentTo(render)
        self.bullet5.reparentTo(render)
                                        
        
        
        
        
        #collision sphere for player bullet
        #regular collision sphere
        cBulletHandler = CollisionHandlerEvent()
        cBulletHandler.setInPattern("bullet-%in")
        
        #problem is coordinate system or parenting
        cSphere = CollisionSphere(0, 0, 0,.2)
        cNodeBullet = CollisionNode("bullet1")
        cNodeBullet = CollisionNode("bullet2")
        cNodeBullet = CollisionNode("bullet3")
        cNodeBullet = CollisionNode("bullet4")
        cNodeBullet = CollisionNode("bullet5")
        cNodeBullet.addSolid(cSphere)
        cNodeBullet.setIntoCollideMask(BitMask32.allOff())
        #cNodeBullet.setCollideMask(0x1+0x2)
        cNodeBulletPath = self.bullet1.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet2.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet3.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet4.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet5.attachNewNode(cNodeBullet)
        
        cNodeBulletPath.show()
        self.cTrav.addCollider(cNodeBulletPath, cBulletHandler)
        
        #add bullet to overall list
        self.bulletList.append(self.bullet1)
        self.bulletList.append(self.bullet2)
        self.bulletList.append(self.bullet3)
        self.bulletList.append(self.bullet4)
        self.bulletList.append(self.bullet5)
        self.bulletTime.append(0)
        self.bulletTime.append(0)
        self.bulletTime.append(0)
        self.bulletTime.append(0)
        self.bulletTime.append(0)
        
    def update(self, task):
        elapsed = task.time - self.prevTime
        #cycle through the bullet list and update the positions
        i = 0
        check = False
        for bullet in self.bulletList:
            angle = deg2Rad(bullet.getH())
            dist = self.speed * elapsed
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            bullet.setPos(bullet.getX() - dx, bullet.getY() - dy, .5)
            self.bulletTime[i] += 1
            if self.bulletTime[i] > 20:
                print('erased')
                bullet.remove()
                self.bulletList.remove(bullet)
                #bullet.getParent().remove()
                self.bulletTime.remove(self.bulletTime[i])
                check = True
            if(check == False):
                i += 1
            else:
                check = False
        self.prevTime = task.time
        return Task.cont
        