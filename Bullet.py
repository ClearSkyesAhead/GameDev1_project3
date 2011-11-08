#bullet class

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random

class Bullet(DirectObject):
    def __init__(self, cTrav):
        #create a constant speed and an overall bullet list to contain all bullets
        self.speed = 100
        self.bulletList = []
        self.bulletTime = []
        self.prevTime = 0
        self.prevBulletTime = 0
        self.cTrav = cTrav
        self.timer = 0
        taskMgr.add(self.updateTimer, "timerUpdate")
        
    def updateTimer(self, task):
        self.timer += task.time
        
    def createBullet(self, bike):
        #load the model and set the pos and H to the bike's
        self.bullet = loader.loadModel("bullet.egg")
        
        #prevent bullet from spawning inside of player collision sphere
        angle = deg2Rad(bike.getH())
        dy = -math.cos(angle) * 5
        dx = math.sin(angle) * 5
        self.bullet.setPos(bike.getX() - dx, bike.getY() - dy, bike.getZ())
        self.bullet.setH(bike.getH())
        self.bullet.setScale(.25)
        self.bullet.reparentTo(render)
        
        #collision sphere for player bullet
        #regular collision sphere
        cBulletHandler = CollisionHandlerEvent()
        cBulletHandler.setInPattern("bullet-%in")
        
        #problem is coordinate system or parenting
        cSphere = CollisionSphere(0, 0, .75,1)
        cNodeBullet = CollisionNode("bullet")
        cNodeBullet.addSolid(cSphere)
        #cNodeBullet.setIntoCollideMask(BitMask32.allOff())
        #cNodeBullet.setCollideMask(0x1+0x2)
        cNodeBulletPath = self.bullet.attachNewNode(cNodeBullet)
        
        cNodeBulletPath.show()
        self.cTrav.addCollider(cNodeBulletPath, cBulletHandler)
        
        #add bullet to overall list
        self.bulletList.append(self.bullet)
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
            if self.bulletTime[i] > 50:
                #print('erased')
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
        