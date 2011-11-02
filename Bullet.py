#bullet class

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random

class Bullet(DirectObject):
    def __init__(self):
        self.speed = .5
        self.bulletList = []
        taskMgr.add(self.update, "bulletTask")
        self.prevTime = 0
        
    def createBullet(self, gun, bike):
        self.bullet = loader.loadModel("temp_bullet.egg")
        self.bullet.reparentTo(gun)
        self.bullet.setPos(gun.getX(), gun.getY(), gun.getZ())
        self.bullet.setH(gun.getH())
        
        self.bulletList.append(self.bullet)
        
    def update(self, task):
        elapsed = task.time - self.prevTime
        for bullet in self.bulletList:
            bullet.reparentTo(render)
            angle = deg2Rad(bullet.getH())
            dist = self.speed * elapsed
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            self.bullet.setPos(self.bullet.getX() - dx, self.bullet.getY() - dy, 0)
        self.prevTime = task.time
        return Task.cont
        