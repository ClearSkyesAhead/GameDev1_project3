#Weapon of some sort

#wall of bullets, because why the hell not

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random

class weapon3(DirectObject):
    def __init__(self, cTrav):
    #create a constant speed and an overall bullet list to contain all bullets
        self.speed = 10
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
        self.bullet1 = loader.loadModel("temp_bullet.egg")
        self.bullet2 = loader.loadModel("temp_bullet.egg")
        self.bullet3 = loader.loadModel("temp_bullet.egg")

        
        self.bullet1.setH(bike.getH())
        self.bullet2.setH(bike.getH())
        self.bullet3.setH(bike.getH())
       
        
        self.bullet1.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet2.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet3.setPos(bike.getX(), bike.getY(), bike.getZ())
        
        self.bullet1.reparentTo(render)
        self.bullet2.reparentTo(render)
        self.bullet3.reparentTo(render)
        
        
        #add bullet to overall list
        self.bulletList.append(self.bullet1)
        self.bulletList.append(self.bullet2)
        self.bulletList.append(self.bullet3)
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
        