#Weapon of some sort

#bullets exlode out of you from all angles

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random

class weapon2(DirectObject):

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
        
        self.bullet1.setH(bike.getH())
        self.bullet2.setH(bike.getH()+20)
        self.bullet3.setH(bike.getH()+40)
        self.bullet4.setH(bike.getH()+60)
        self.bullet5.setH(bike.getH()+80)
        self.bullet6.setH(bike.getH()+100)
        self.bullet7.setH(bike.getH()+120)
        self.bullet8.setH(bike.getH()+140)
        self.bullet9.setH(bike.getH()+160)
        self.bullet10.setH(bike.getH()+180)
        self.bullet11.setH(bike.getH()+200)
        self.bullet12.setH(bike.getH()+220)
        self.bullet13.setH(bike.getH()+240)
        self.bullet14.setH(bike.getH()+260)
        self.bullet15.setH(bike.getH()+280)
        self.bullet16.setH(bike.getH()+300)
        self.bullet17.setH(bike.getH()+320)
        self.bullet18.setH(bike.getH()+340)
        
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
        cNodeBullet = CollisionNode("bullet6")
        cNodeBullet = CollisionNode("bullet7")
        cNodeBullet = CollisionNode("bullet8")
        cNodeBullet = CollisionNode("bullet9")
        cNodeBullet = CollisionNode("bullet10")
        cNodeBullet = CollisionNode("bullet11")
        cNodeBullet = CollisionNode("bullet12")
        cNodeBullet = CollisionNode("bullet13")
        cNodeBullet = CollisionNode("bullet14")
        cNodeBullet = CollisionNode("bullet15")
        cNodeBullet = CollisionNode("bullet16")
        cNodeBullet = CollisionNode("bullet17")
        cNodeBullet = CollisionNode("bullet18")

        cNodeBullet.addSolid(cSphere)
        cNodeBullet.setIntoCollideMask(BitMask32.allOff())
        #cNodeBullet.setCollideMask(0x1+0x2)
        cNodeBulletPath = self.bullet1.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet2.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet3.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet4.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet5.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet6.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet7.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet8.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet9.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet10.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet11.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet12.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet13.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet14.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet15.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet16.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet17.attachNewNode(cNodeBullet)
        cNodeBulletPath = self.bullet18.attachNewNode(cNodeBullet)

        
        
        cNodeBulletPath.show()
        self.cTrav.addCollider(cNodeBulletPath, cBulletHandler)
        
        
        
        
        
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
        