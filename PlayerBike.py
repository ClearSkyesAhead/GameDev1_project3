#player bike class

#importing all the panda stuff since I'm not sure which ones i need

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random
from Bullet import Bullet 

class PlayerBike(DirectObject):
    def __init__(self, cTrav):
        #create speed vars
        self.max_vel = 10
        self.accel = .5
        self.current_vel = 0
        self.cTrav = cTrav
        
        #create empty list for bullets and a task for updating the positions
        self.bulletList = []
        self.bullet = Bullet(cTrav)
        taskMgr.add(self.bullet.update, "bulletTask")
    
        
        #load the bike actor and parent it to a physics node
        self.bike = Actor("temp_bike.egg", {"move":"bike-move", "shoot":"bike-shoot"})
        self.bike.reparentTo(render)
        
        #load the gun actors
        self.gun1 = Actor("temp_gun.egg", {"shoot":"gun-shoot"})
        self.gun1.reparentTo(self.bike)
        self.gun1.setPos(-.5, 0, .5)
        self.gun1.setH(180)
        
        self.gun2 = Actor("temp_gun.egg", {"shoot":"gun-shoot"})
        self.gun2.reparentTo(self.bike)
        self.gun2.setPos(.46, 0, 1)
        self.gun2.setH(180)
        self.gun2.setR(180)
        
        #load the headlight models
        self.headlight1 = loader.loadModel("temp_light.egg")
        self.headlight1.reparentTo(self.bike)
        self.headlight1.setPos(.3, .55, .4)
        self.headlight1.setScale(.75)
        
        #load the headlight models
        self.headlight2 = loader.loadModel("temp_light.egg")
        self.headlight2.reparentTo(self.bike)
        self.headlight2.setPos(-.3, .55, .4)
        self.headlight2.setScale(.75)
        
        #setup a move task for the bike
        taskMgr.add(self.move, "moveTask")
        self.prevTime = 0
        self.isMoving = False
        
        #setup a shoot task for the bike
        taskMgr.add(self.shoot, "shootTask")
        self.shotClock = 25
        # for shooting anim self.isShooting = False
        
        #setup a moving dictionary
        self.moveMap = {"left":0, "right":0, "forward":0}
        
        #setup a shoot check
        self.shootCheck = 0
        
        #pusher collision sphere
        collisionPusher = CollisionHandlerPusher()
        collisionPusher.setInPattern("p_bike-%in")
        cPushSphere = CollisionSphere((0,0.2,1),1)
        
        cNode = CollisionNode("p_bike_push")
        cNode.addSolid(cPushSphere)
        cNode.setIntoCollideMask(BitMask32.allOff())
        cNodePath = self.bike.attachNewNode(cNode)
        
        cNodePath.show()
        
        collisionPusher.addCollider(cNodePath, self.bike)
        self.cTrav.addCollider(cNodePath, collisionPusher)
        
        
        #test sphere
        cTestSphere = CollisionSphere((3,3,0),1)
        cNodeTest = CollisionNode("test")
        cNodeTest.addSolid(cTestSphere)
        cNodeTestPath = render.attachNewNode(cNodeTest)
        cNodeTestPath.show()
        
        
        
        
        #setup and parent spotlights to the player
        self.spotlight1 = Spotlight("headlight1")
        self.spotlight1.setColor((1, 1, 1, 1))
        lens = PerspectiveLens()
        #can change size of cone
        lens.setFov(20)
        self.spotlight1.setLens(lens)
        self.spotlight1.setExponent(100)
        lightNode = self.headlight1.attachNewNode(self.spotlight1)
        render.setLight(lightNode)
        
        self.spotlight2 = Spotlight("headlight2")
        self.spotlight2.setColor((1, 1, 1, 1))
        self.spotlight2.setLens(lens)
        self.spotlight2.setExponent(100)
        lightNode = self.headlight2.attachNewNode(self.spotlight2)
        render.setLight(lightNode)
    
    def setDirection(self, key, value):
        #set the direction as on or off
        self.moveMap[key] = value
        
    def setShoot(self, value):
        
        self.shootCheck = value
        print("set shoot =", self.shootCheck)
    
    def shoot(self, task):
        #check if space bar is pressed
        if self.shootCheck:
            #check if able to shoot
            if self.shotClock >= 25:
                print("Shooting a bullet!")
                #create a bullet
                self.bullet.createBullet(self.bike)
                self.shotClock = 0
            else:
                self.shotClock += 1
        else:
            self.shotClock += 1
        return Task.cont
        
    def move(self, task):
        elapsed = task.time - self.prevTime
        
        #check key map
        if self.moveMap['left']:
            self.bike.setH(self.bike.getH() + elapsed * 100)
        if self.moveMap['right']:
            self.bike.setH(self.bike.getH() - elapsed * 100)
        if self.moveMap['forward']:
            self.current_vel += self.accel
            if(self.current_vel > self.max_vel):
                self.current_vel = self.max_vel
            dist = self.current_vel * elapsed
            angle = deg2Rad(self.bike.getH())
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            self.bike.setPos(self.bike.getX() - dx, self.bike.getY() - dy, 0)
        else:
            self.current_vel -= 10 * self.accel * elapsed
            if(self.current_vel < 0):
                self.current_vel = 0
            dist = self.current_vel * elapsed
            angle = deg2Rad(self.bike.getH())
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            self.bike.setPos(self.bike.getX() - dx, self.bike.getY() - dy, 0)
        
        if self.moveMap['left'] or self.moveMap['right'] or self.moveMap['forward']:
            if self.isMoving == False:
                self.isMoving = True
                #self.bike.loop("walk")
        else:
            if self.isMoving:
                self.isMoving = False
                self.bike.stop()
                #self.bike.pose("walk", 4)
        
        self.prevTime = task.time
        #print(self.current_vel)
        return Task.cont
        
    def setupCollisions(self):
        pass
        
        