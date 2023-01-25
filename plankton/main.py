from manager import Manager
from plankton_client import Client,Command, KICK
from sys import argv
from math import atan2
import numpy as np


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

class ExampleManager(Manager):
    def step(self):
        self.setSideValue()
        # self.go_to(self.allies1, x=0.0, y=0.0, orientation=0.0)
        # self.control(self.allies2, forward_velocity=1.0, left_velocity=0.0, angular_velocity=0.0)
        # self.client.commands.append(Command(id=0, forward_velocity=1.0, angular_velocity=0.0))
        # print(self.ball)
        toTarget = self.goalTarget() - self.ball
        toTarget = -(normalize(toTarget)*0.1)
        shootingPos = toTarget + self.ball

        kick = KICK.STRAIGHT_KICK if self.distToBall() < 0.11 else KICK.NO_KICK

        self.go_to(self.allies1, x=shootingPos[0], y=shootingPos[1], orientation=self.angleTo(self.allies1.position, self.ball), kick=kick, power=1)

    def distToBall(self):
        return np.linalg.norm(self.allies1.position - self.ball)

    def goalTarget(self):
        x = -self.allies1.side * self.field['length']/2
        y = 0
        return np.array([x,y])

    def setSideValue(self):
        if not hasattr(self.allies1, "side"): 
            self.allies1.side = 1 if self.allies1.position[0] > 0 else -1
    
    def angleTo(self, p1, p2):
        v = p1 - p2
        return atan2(-v[1], -v[0])


if __name__ == "__main__":
    is_yellow = len(argv) > 1 and argv[1] == '-y'
    with Client(is_yellow) as client:
        manager = ExampleManager(client=client)
        manager.run()