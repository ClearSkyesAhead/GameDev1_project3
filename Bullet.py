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
        #create a constant speed and an overall bullet list to contain all bullets
        self.speed = .5
        self.bulletList = []
        self.prevTime = 0
        
    def createBullet(self, gun, bike):
        #load the model and set the pos and H to the bike's
        self.bullet = loader.loadModel("temp_bullet.egg")
        self.bullet.setPos(bike.getX(), bike.getY(), bike.getZ())
        self.bullet.setH(bike.getH())
        self.bullet.reparentTo(render)
        #add bullet to overall list
        self.bulletList.append(self.bullet)
        
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
        