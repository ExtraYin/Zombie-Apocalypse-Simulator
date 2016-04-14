"""
@author: Yida Yin

Copyright (c) 16/3/17 Yida Yin. All rights reserved.
"""

import machine
import settings
import traits


class World(object):

    def __init__(self):
        self.month = 0
        self.humans = []
        self.zombies = []

    def isHuman(self, x, y):
        for human in self.humans:
            if x == human.m_X and y == human.m_Y:
                return True
        return False

    def isZombie(self, x, y):
        for zombie in self.zombies:
            if x == zombie.m_X and y == zombie.m_Y:
                return True
        return False

    def isValid(self, x, y):
        if x < 0 or x >= settings.CITY_SIZE:
            return False
        if y < 0 or y >= settings.CITY_SIZE:
            return False
        return True

    def isPassable(self, x, y):
        return self.isValid(x, y) and (not self.isZombie(x, y)) and (not self.isHuman(x ,y))

    def attack(self, x, y, infect, attacker):
        # kill anything at location, if zombie attack spawn a new zombie at location
        assert(isinstance(attacker, machine.MachineState))
        if not infect:
            # nothing happens if zombie attacks zombie
            for i, zombie in enumerate(self.zombies):
                # check zombie first, so if turned the new zombie won't be killed/ take turn
                if zombie.m_X == x and zombie.m_Y == y:
                    # delete the zombie
                    del self.zombies[i]  # Don't worry. It's fine to use for loop here.
                    break
        for i, human in enumerate(self.humans):
            if human.m_X == x and human.m_Y == y:
                if infect:
                    # infect him
                    assert(isinstance(attacker.m_Traits, traits.ZombieTraits))
                    new_zombie = machine.MachineState()
                    new_zombie.m_X = x
                    new_zombie.m_Y = y
                    new_zombie.m_Facing = human.m_Facing
                    new_zombie.m_Traits = traits.ZombieTraits()
                    new_zombie.m_Machine.m_Ops = attacker.m_Machine.m_Ops[:]
                    new_zombie.m_Machine.name = attacker.m_Machine.name
                    self.zombies.append(new_zombie)
                    del self.humans[i]  # Don't worry. It's fine to use for loop here.
                    break
                else:
                    # kill him
                    del self.humans[i]

    def newGame(self):
        self.month = 0
        self.humans = []
        self.zombies = []