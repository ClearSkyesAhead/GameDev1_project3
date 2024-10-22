#terrain class

#importing all the panda stuff since I'm not sure which ones i need

import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random

class Terrain(DirectObject):
    def __init__(self):
        #load the wall terrain model
        self.wall_terrain = loader.loadModel("wall_terrain.egg")
        self.wall_terrain.reparentTo(render)
        self.wall_terrain.setScale(.85)
        
        
        #load the jumps and floor terrain model
        self.ground_terrain = loader.loadModel("ground_terrain.egg")
        self.ground_terrain.reparentTo(render)
        self.ground_terrain.setScale(.85)
        
        #set a collide mask
        #self.terrain.setCollideMask(BitMask32.allOff())
        #self.terrain.setCollideMask(BitMask32.bit(0))
        self.ground_terrain.setCollideMask(2)
        self.wall_terrain.setCollideMask(1)
        
        taskMgr.add(self.powerUpUpdate, "powerUpTask")
        
        #setup walls
        #wall1
        wall1 = CollisionPlane(Plane(Vec3(-1, 0, 0), Point3(82, -77, 77)))
        cNodeWall1 = CollisionNode("wall1")
        cNodeWall1.addSolid(wall1)
        cNodeWall1.setIntoCollideMask(1)
        self.cNodePathWall1 = render.attachNewNode(cNodeWall1)
        #self.cNodePathWall1.show()
        
        #wall 2
        wall2 = CollisionPlane(Plane(Vec3(1, 0, 0), Point3(-82, -77, 77)))
        cNodeWall2 = CollisionNode("wall2")
        cNodeWall2.addSolid(wall2)
        cNodeWall2.setIntoCollideMask(1)
        self.cNodePathWall2 = render.attachNewNode(cNodeWall2)
        #self.cNodePathWall2.show()
        
        #wall3
        wall3 = CollisionPlane(Plane(Vec3(0, -1, 0), Point3(82, 82, 77)))
        cNodeWall3 = CollisionNode("wall3")
        cNodeWall3.addSolid(wall3)
        cNodeWall3.setIntoCollideMask(1)
        self.cNodePathWall3 = render.attachNewNode(cNodeWall3)
        #self.cNodePathWall3.show()
        
        #wall4
        wall4 = CollisionPlane(Plane(Vec3(0, 1, 0), Point3(82, -82, 77)))
        cNodeWall4 = CollisionNode("wall4")
        cNodeWall4.addSolid(wall4)
        cNodeWall4.setIntoCollideMask(1)
        self.cNodePathWall4 = render.attachNewNode(cNodeWall4)
        #self.cNodePathWall4.show()
        
        
        #setup power up collision spheres and the associated model
        
        #powerup1 collision sphere (invincibility)
        self.shield = Actor('shield.egg', {'rotate':'shield_anim.egg'})
        self.shield.reparentTo(render)
        self.shield.setPos(0, -.3, 16.5)
        self.shield.setScale(0.5)
        self.shield.loop('rotate')
        
        cPowerSphere1 = CollisionSphere((0,0,0),8)
        cPowerNode1 = CollisionNode("powerup1")
        cPowerNode1.addSolid(cPowerSphere1)
        cPowerNode1.setIntoCollideMask(1)
        self.cPowerNode1Path = self.shield.attachNewNode(cPowerNode1)
        #self.cPowerNode1Path.show()
        self.powerUp1 = True
        self.powerUp1Count = 0
        
        #powerup2 collision sphere (matched with powerup3)
        self.shotgun = Actor('shotgun.egg', {'rotate':'shotgun_anim.egg'})
        self.shotgun.reparentTo(render)
        self.shotgun.setPos(.5, 77, 18.5)
        self.shotgun.setScale(0.5)
        self.shotgun.loop('rotate')
        
        cPowerSphere2 = CollisionSphere((0,0,0),8)
        cPowerNode2 = CollisionNode("powerup2")
        cPowerNode2.addSolid(cPowerSphere2)
        cPowerNode2.setIntoCollideMask(1)
        self.cPowerNode2Path = self.shotgun.attachNewNode(cPowerNode2)
        #self.cPowerNode2Path.show()
        self.powerUp2 = True
        self.powerUp2Count = 0
        
        #powerup3 collision sphere (matched with powerup2)
        self.shotgun2 = Actor('shotgun.egg', {'rotate':'shotgun_anim.egg'})
        self.shotgun2.reparentTo(render)
        self.shotgun2.setPos(.5, -77, 18.5)
        self.shotgun2.setScale(0.5)
        self.shotgun2.loop('rotate')
        
        cPowerSphere3 = CollisionSphere((0,0,0),8)
        cPowerNode3 = CollisionNode("powerup3")
        cPowerNode3.addSolid(cPowerSphere3)
        cPowerNode3.setIntoCollideMask(1)
        self.cPowerNode3Path = self.shotgun2.attachNewNode(cPowerNode3)
        #self.cPowerNode3Path.show()
        self.powerUp3 = True
        self.powerUp3Count = 0
        
        #powerup4 collision sphere (matched with powerup5)
        self.health = Actor('health.egg', {'rotate':'health_anim.egg'})
        self.health.reparentTo(render)
        self.health.setPos(77, -1, 18.5)
        self.health.setScale(0.5)
        self.health.loop('rotate')
        
        cPowerSphere4 = CollisionSphere((0,0,0),8)
        cPowerNode4 = CollisionNode("powerup4")
        cPowerNode4.addSolid(cPowerSphere4)
        cPowerNode4.setIntoCollideMask(1)
        self.cPowerNode4Path = self.health.attachNewNode(cPowerNode4)
        #self.cPowerNode4Path.show()
        self.powerUp4 = True
        self.powerUp4Count = 0
        
        #powerup5 collision sphere (matched with powerup4)
        self.health2 = Actor('health.egg', {'rotate':'health_anim.egg'})
        self.health2.reparentTo(render)
        self.health2.setPos(-77, -1, 18.5)
        self.health2.setScale(0.5)
        self.health2.loop('rotate')
        
        cPowerSphere5 = CollisionSphere((0,0,0),8)
        cPowerNode5 = CollisionNode("powerup5")
        cPowerNode5.addSolid(cPowerSphere5)
        cPowerNode5.setIntoCollideMask(1)
        self.cPowerNode5Path = self.health2.attachNewNode(cPowerNode5)
        #self.cPowerNode5Path.show()
        self.powerUp5 = True
        self.powerUp5Count = 0
        
        #setup lights for outer box
        plight5 = PointLight('plight1')
        plight5.setColor(VBase4(1,1,1,1))
        plight5.setAttenuation(Point3(0,0,.01))
        plnp5 = render.attachNewNode(plight5)
        plnp5.setPos(-37.5,39.5,13.5)
        render.setLight(plnp5)
        
        plight6 = PointLight('plight1')
        plight6.setColor(VBase4(1,1,1,1))
        plight6.setAttenuation(Point3(0,0,.01))
        plnp6 = render.attachNewNode(plight6)
        plnp6.setPos(37.5,39.5,13.5)
        render.setLight(plnp6)
        
        plight7 = PointLight('plight1')
        plight7.setColor(VBase4(1,1,1,1))
        plight7.setAttenuation(Point3(0,0,.01))
        plnp7 = render.attachNewNode(plight7)
        plnp7.setPos(37.5,-39.5,13.5)
        render.setLight(plnp7)
        
        plight8 = PointLight('plight1')
        plight8.setColor(VBase4(1,1,1,1))
        plight8.setAttenuation(Point3(0,0,.01))
        plnp8 = render.attachNewNode(plight8)
        plnp8.setPos(-37.5,-39.5,13.5)
        render.setLight(plnp8)

    def powerUpUpdate(self, task):
        #check powerup1
        if self.powerUp1 == False:
            #print('increasing count')
            self.powerUp1Count += 1
        if self.powerUp1Count == 500:
            #print('making a new one')
            self.powerUp1 = True
            self.powerUp1Count = 0
            self.shield = Actor('shield.egg', {'rotate':'shield_anim.egg'})
            self.shield.reparentTo(render)
            self.shield.setPos(0, -.3, 16.5)
            self.shield.setScale(0.5)
            self.shield.loop('rotate')
            
            cPowerSphere1 = CollisionSphere((0,0,0),8)
            cPowerNode1 = CollisionNode("powerup1")
            cPowerNode1.addSolid(cPowerSphere1)
            cPowerNode1.setIntoCollideMask(1)
            self.cPowerNode1Path = self.shield.attachNewNode(cPowerNode1)
        
        #check powerup2
        if self.powerUp2 == False:
            #print('increasing count')
            self.powerUp2Count += 1
        if self.powerUp2Count == 250:
            #print('making a new one')
            self.powerUp2 = True
            self.powerUp2Count = 0
            self.shotgun = Actor('shotgun.egg', {'rotate':'shotgun_anim.egg'})
            self.shotgun.reparentTo(render)
            self.shotgun.setPos(.5, 77, 18.5)
            self.shotgun.setScale(0.5)
            self.shotgun.loop('rotate')
            
            cPowerSphere2 = CollisionSphere((0,0,0),8)
            cPowerNode2 = CollisionNode("powerup2")
            cPowerNode2.addSolid(cPowerSphere2)
            cPowerNode2.setIntoCollideMask(1)
            self.cPowerNode2Path = self.shotgun.attachNewNode(cPowerNode2)
            
        #check powerup3
        if self.powerUp3 == False:
            #print('increasing count')
            self.powerUp3Count += 1
        if self.powerUp3Count == 250:
            #print('making a new one')
            self.powerUp3 = True
            self.powerUp3Count = 0
            self.shotgun2 = Actor('shotgun.egg', {'rotate':'shotgun_anim.egg'})
            self.shotgun2.reparentTo(render)
            self.shotgun2.setPos(.5, -77, 18.5)
            self.shotgun2.setScale(0.5)
            self.shotgun2.loop('rotate')
            
            cPowerSphere3 = CollisionSphere((0,0,0),8)
            cPowerNode3 = CollisionNode("powerup3")
            cPowerNode3.addSolid(cPowerSphere3)
            cPowerNode3.setIntoCollideMask(1)
            self.cPowerNode3Path = self.shotgun2.attachNewNode(cPowerNode3)
            
        #check powerup4
        if self.powerUp4 == False:
            #print('increasing count')
            self.powerUp4Count += 1
        if self.powerUp4Count == 250:
            #print('making a new one')
            self.powerUp4 = True
            self.powerUp4Count = 0
            self.health = Actor('health.egg', {'rotate':'health_anim.egg'})
            self.health.reparentTo(render)
            self.health.setPos(77, -1, 18.5)
            self.health.setScale(0.5)
            self.health.loop('rotate')
            
            cPowerSphere4 = CollisionSphere((0,0,0),8)
            cPowerNode4 = CollisionNode("powerup4")
            cPowerNode4.addSolid(cPowerSphere4)
            cPowerNode4.setIntoCollideMask(1)
            self.cPowerNode4Path = self.health.attachNewNode(cPowerNode4)
            
        #check powerup5
        if self.powerUp5 == False:
            #print('increasing count')
            self.powerUp5Count += 1
        if self.powerUp5Count == 250:
            #print('making a new one')
            self.powerUp5 = True
            self.powerUp5Count = 0
            self.health2 = Actor('health.egg', {'rotate':'health_anim.egg'})
            self.health2.reparentTo(render)
            self.health2.setPos(-77, -1, 18.5)
            self.health2.setScale(0.5)
            self.health2.loop('rotate')
            
            cPowerSphere5 = CollisionSphere((0,0,0),8)
            cPowerNode5 = CollisionNode("powerup5")
            cPowerNode5.addSolid(cPowerSphere5)
            cPowerNode5.setIntoCollideMask(1)
            self.cPowerNode5Path = self.health2.attachNewNode(cPowerNode5)
        return Task.cont
