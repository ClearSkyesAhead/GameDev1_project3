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
        self.max_vel = 35
        self.accel = 2
        self.current_vel = 0
        self.cTrav = cTrav
        
        #vars for jumping
        self.tempHeading = 0
        self.temp_vel = 0
        self.count = 0
        self.first_time = False
        self.jump = False
        self.dz = 0
        
        #set HP
        self.hp = 10
        
        #invincible check
        self.invin = False
        self.invinCount = 0
        
        #load all sound files
        self.singleShot = base.loader.loadSfx('M4A1.mp3')
        
        
        #create empty list for bullets and a task for updating the positions
        self.bullet = Bullet(cTrav)
        taskMgr.add(self.bullet.update, "bulletTask")
        taskMgr.add(self.updatePowerup, "powerupTask")
    
        
        #load the bike actor and parent it to a physics node
        self.bike = Actor("motorcycle2.egg", {"move":"moto2_moveAnimation.egg", "turnL":"moto2_blahblah.egg"})
        #self.bike.setScale(.5)
        #self.bike.setH(180)
        self.bike.reparentTo(render)
        
        
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
        

        #setup a wall collision check
        self.wallCheck = False
        
        #pusher collision spheres
        #front
        collisionPusher = CollisionHandlerPusher()
        collisionPusher.setInPattern("p_bike-%in")
        cPushSphere = CollisionSphere((0,3.5,2),2)
        
        cNode1 = CollisionNode("p_bike_push")
        cNode1.addSolid(cPushSphere)
        cNode1.setIntoCollideMask(0x10)
        cNode1.setFromCollideMask(0x1)
        self.cNodePath1 = self.bike.attachNewNode(cNode1)
        
        #self.cNodePath1.show()
        
        collisionPusher.addCollider(self.cNodePath1, self.bike)
        self.cTrav.addCollider(self.cNodePath1, collisionPusher)
        
        #middle
        cPushSphere = CollisionSphere((0,0,2),2)
        
        cNode2 = CollisionNode("p_bike_push")
        cNode2.addSolid(cPushSphere)
        cNode2.setIntoCollideMask(0x10)
        cNode2.setFromCollideMask(0x1)
        self.cNodePath2 = self.bike.attachNewNode(cNode2)
        
        #self.cNodePath2.show()
        
        collisionPusher.addCollider(self.cNodePath2, self.bike)
        self.cTrav.addCollider(self.cNodePath2, collisionPusher)
        
        #back
        cPushSphere = CollisionSphere((0,-2.5,2),2)
        
        cNode3 = CollisionNode("p_bike_push")
        cNode3.addSolid(cPushSphere)
        cNode3.setIntoCollideMask(0x10)
        cNode3.setFromCollideMask(0x1)
        self.cNodePath3 = self.bike.attachNewNode(cNode3)
        
        #self.cNodePath3.show()
        
        collisionPusher.addCollider(self.cNodePath3, self.bike)
        self.cTrav.addCollider(self.cNodePath3, collisionPusher)
        
        #collision rays for faux-gravity
        #front wheel
        lifter = CollisionHandlerFloor()
        lifter.setMaxVelocity(9.8)
        
        cRay1 = CollisionRay(0, 3, 1, 0, 0, -1)
        cRayNode1 = CollisionNode('playerRay')
        cRayNode1.addSolid(cRay1)
        cRayNode1.setIntoCollideMask(BitMask32.allOff())
        cRayNode1.setFromCollideMask(2)
        cRayNodePath1 = self.bike.attachNewNode(cRayNode1)
        cRayNodePath1.show()
         
        self.cTrav.addCollider(cRayNodePath1, lifter)
        lifter.addCollider(cRayNodePath1, self.bike)
        
        #setup and parent spotlights to the player
        self.spotlight = Spotlight("headlight")
        self.spotlight.setColor((1, 1, 1, 1))
        self.spotlight.setAttenuation(Point3(0,0,.001))
        lens = PerspectiveLens()
        #can change size of cone
        lens.setFov(20)
        self.spotlight.setLens(lens)
        self.spotlight.setExponent(100)
        lightNode = self.bike.attachNewNode(self.spotlight)
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
                #print("Shooting a bullet!")
                #create a bullet
                self.singleShot.play()
                self.bullet.createBullet(self.bike)
                self.shotClock = 0
            else:
                self.shotClock += 1
        else:
            self.shotClock += 1
        return Task.cont
    
    def updatePowerup(self, task):
        #check powerup timers
        if self.invin == True:
            self.invinCount += 1
        if self.invinCount == 30:
            self.invin = False
            self.invinCount = 0
        return Task.cont
    def move(self, task):
        elapsed = task.time - self.prevTime
        
        #keep track of all the bike's previous Pos and Hpr
        prevX = self.bike.getX()
        prevY = self.bike.getY()
        prevZ = self.bike.getZ()
        prevH = self.bike.getH()
        prevP = self.bike.getP()
        prevR = self.bike.getR()
        
        #check key map
        
        #check if at jump height
        if prevZ >= 4.5:
            #set jump check
            self.jump = True
            
            #check for when temp_vel needs to be increased instead of decreased
            if self.first_time == False:
                self.temp_vel -= 9.8
            if self.temp_vel <= 0 and self.first_time == False:
                self.first_time = True
                self.temp_vel += 9.8
            elif self.first_time == True:
                self.temp_vel += 9.8
                
            #make sure temp_vel doesn't increase too much
            if self.temp_vel > self.current_vel:
                self.temp_vel = self.current_vel
                
            #calculate dist for dy and dx normally, then do trig for dz
            dist = (self.current_vel + 11) * elapsed
            angle = deg2Rad(self.bike.getH())
            dy = dist * -math.cos(angle)
            dx = dist * math.sin(angle)
            self.dz = math.sqrt((dy*dy)+(dx*dx))
            
            #debug prints
            """print('new')
            print('dy', dy)
            print('dx', dx)
            print('dz', dz)
            print('angle', angle)
            print('bike heading', self.bike.getH())
            print('bike x', self.bike.getX())
            print('bike y', self.bike.getY())
            print('temp_vel', self.temp_vel)"""
            
            #use a count to determine when to decrease or increase the bike's Z
            if self.count < 30:
                self.bike.setPos(self.bike.getX() - dx, self.bike.getY() - dy, self.bike.getZ() + self.dz)
            else:
                self.bike.setPos(self.bike.getX() - dx, self.bike.getY() - dy, self.bike.getZ() - self.dz)
            self.count += 1
            
        else:
            #reset counters used in jumping
            self.first_time = False
            self.count = 0
            
            #check if turning
            if self.moveMap['left']:
                self.bike.setH(self.bike.getH() + elapsed * 150)
            if self.moveMap['right']:
                self.bike.setH(self.bike.getH() - elapsed * 150)
                
            #check keymap for forward motion
            #accelerate
            if self.moveMap['forward']:
                #print(prevZ)
                self.current_vel += self.accel
                self.temp_vel = self.current_vel
                if(self.current_vel > self.max_vel):
                    self.current_vel = self.max_vel
                dist = self.current_vel * elapsed
                angle = deg2Rad(self.bike.getH())
                dx = dist * math.sin(angle)
                dy = dist * -math.cos(angle)
                if self.jump == True:
                    self.bike.setPos(self.bike.getX() - dx, self.bike.getY() - dy, self.bike.getZ() - self.dz)
                    if self.bike.getZ() <= 0:
                        self.jump = False
                        self.bike.setZ(0)
                else:
                    self.bike.setPos(self.bike.getX() - dx, self.bike.getY() - dy, self.bike.getZ())
                
                
            else:
                #decelerate
                self.current_vel -= 20 * self.accel * elapsed
                self.temp_vel = self.current_vel
                if(self.current_vel < 0):
                    self.current_vel = 0
                dist = self.current_vel * elapsed
                angle = deg2Rad(self.bike.getH())
                dx = dist * math.sin(angle)
                dy = dist * -math.cos(angle)
                if self.jump == True:
                    self.bike.setPos(self.bike.getX() - dx, self.bike.getY() - dy, self.bike.getZ() - self.dz)
                    if self.bike.getZ() <= 0:
                        self.jump = False
                        self.bike.setZ(0)
                else:
                    self.bike.setPos(self.bike.getX() - dx, self.bike.getY() - dy, self.bike.getZ())
        
        #attempt to change pitch
        if self.bike.getZ() != prevZ:
            ang = math.atan2(self.bike.getY(), self.bike.getZ())
            self.bike.setP(ang)
            
        if self.moveMap['left'] or self.moveMap['right'] or self.moveMap['forward']:
            #print('heading', self.bike.getH())
            if self.isMoving == False:
                self.isMoving = True
                self.bike.loop("move")
        else:
            if self.isMoving:
                self.isMoving = False
                self.bike.stop()
                #self.bike.pose("walk", 4)
        
        self.prevTime = task.time
        #print(self.current_vel)
        return Task.cont
        