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
    def __init__(self):

        #create a constant speed and an overall bullet list to contain all bullets
        self.speed = 10
        self.bulletList = []
        self.prevTime = 0
        
    def createBullet(self, bike):
        #load the model and set the pos and H to the bike's
        self.bullet1 = loader.loadModel("temp_bullet.egg")
        self.bullet2 = loader.loadModel("temp_bullet.egg")
        self.bullet3 = loader.loadModel("temp_bullet.egg")
        self.bullet4 = loader.loadModel("temp_bullet.egg")
        self.bullet5 = loader.loadModel("temp_bullet.egg")
        self.bullet6 = loader.loadModel("temp_bullet.egg")
        self.bullet7 = loader.loadModel("temp_bullet.egg")
        self.bullet8 = loader.loadModel("temp_bullet.egg")
        self.bullet9 = loader.loadModel("temp_bullet.egg")
        self.bullet10 = loader.loadModel("temp_bullet.egg")
        self.bullet11 = loader.loadModel("temp_bullet.egg")
        self.bullet12 = loader.loadModel("temp_bullet.egg")
        self.bullet13 = loader.loadModel("temp_bullet.egg")
        self.bullet14 = loader.loadModel("temp_bullet.egg")
        self.bullet15 = loader.loadModel("temp_bullet.egg")
        self.bullet16 = loader.loadModel("temp_bullet.egg")
        self.bullet17 = loader.loadModel("temp_bullet.egg")
        self.bullet18 = loader.loadModel("temp_bullet.egg")
        
        self.bullet1.setH(bike.getH())
        self.bullet2.setH(bike.getH())
        self.bullet3.setH(bike.getH())
        self.bullet4.setH(bike.getH())
        self.bullet5.setH(bike.getH())
        self.bullet6.setH(bike.getH())
        self.bullet7.setH(bike.getH())
        self.bullet8.setH(bike.getH())
        self.bullet9.setH(bike.getH())
        self.bullet10.setH(bike.getH())
        self.bullet11.setH(bike.getH())
        self.bullet12.setH(bike.getH())
        self.bullet13.setH(bike.getH())
        self.bullet14.setH(bike.getH())
        self.bullet15.setH(bike.getH())
        self.bullet16.setH(bike.getH())
        self.bullet17.setH(bike.getH())
        self.bullet18.setH(bike.getH())
        
        self.bullet1.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet2.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet3.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet4.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet5.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet6.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet7.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet8.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet9.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet10.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet11.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet12.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet13.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet14.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet15.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet16.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet17.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet18.setPos(bike.getX(), bike.getY(), bike.getZ())
        
        self.bullet1.reparentTo(render)
        self.bullet2.reparentTo(render)
        self.bullet3.reparentTo(render)
        self.bullet4.reparentTo(render)
        self.bullet5.reparentTo(render)
        self.bullet6.reparentTo(render)
        self.bullet7.reparentTo(render)
        self.bullet8.reparentTo(render)
        self.bullet9.reparentTo(render)
        self.bullet10.reparentTo(render)
        self.bullet11.reparentTo(render)
        self.bullet12.reparentTo(render)
        self.bullet13.reparentTo(render)
        self.bullet14.reparentTo(render)
        self.bullet15.reparentTo(render)
        self.bullet16.reparentTo(render)
        self.bullet17.reparentTo(render)
        self.bullet18.reparentTo(render)
        
        #add bullet to overall list
        self.bulletList.append(self.bullet1)
        self.bulletList.append(self.bullet2)
        self.bulletList.append(self.bullet3)
        self.bulletList.append(self.bullet4)
        self.bulletList.append(self.bullet5)
        self.bulletList.append(self.bullet6)
        self.bulletList.append(self.bullet7)
        self.bulletList.append(self.bullet8)
        self.bulletList.append(self.bullet9)
        self.bulletList.append(self.bullet10)
        self.bulletList.append(self.bullet11)
        self.bulletList.append(self.bullet12)
        self.bulletList.append(self.bullet13)
        self.bulletList.append(self.bullet14)
        self.bulletList.append(self.bullet15)
        self.bulletList.append(self.bullet16)
        self.bulletList.append(self.bullet17)
        self.bulletList.append(self.bullet18)
        
        
    def update(self, task):
        elapsed = task.time - self.prevTime
        #cycle through the bullet list and update the positions
        for bullet in self.bulletList:
            angle = deg2Rad(bullet.getH())
            dist = self.speed * elapsed
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)

            bullet.setPos(bullet.getX() - dx, bullet.getY() - dy, .5)
            
        self.prevTime = task.time
        return Task.cont
        