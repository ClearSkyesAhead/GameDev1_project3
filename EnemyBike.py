#enemy bike class

from Bike import Bike

from panda3d.ai import *

class EnemyBike(Bike):
    def __init__(self):
        Bike.__init__(self)
        self.initAI()
		
    def initAI(self):
        self.AIchar = AICharacter("Enemy Bike", self.bike, 100, 0.05, 10)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
 
        #self.AIbehaviors.pursue(self.p_bike.bike, 0.7)
        self.AIbehaviors.wander(5.0, 1, 10, 0.3)
        #self.AIbehaviors.obstacleAvoidance(1.0)
        #self.e_bike.loop("run")
		
    def update(self):
        """if self.lights:
            self.lightsOff()
        else:
            self.lightsOn()"""
            