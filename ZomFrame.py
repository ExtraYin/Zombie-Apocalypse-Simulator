"""
@author: Yida Yin

Copyright (c) 16/3/18 Yida Yin. All rights reserved.
"""

from world import World
from machine import MachineState, Machine
from traits import ZombieTraits, HumanTraits
import settings
import random
import time


class ZomFrame(object):
    def __init__(self):
        self.racoonCity = World()
        self.new_game("./zom/eric_Zombie.zom", "./zom/deer.zom")

    def generate_zombies(self, city, file_path):
        # generate zombies
        assert isinstance(city, World)
        for i in range(settings.NUMBER_OF_ZOMBIES):
            zombieMachineState = MachineState()
            zombieMachineState.m_Traits = ZombieTraits()
            # get a passable random location
            while True:
                x = random.randrange(0, settings.CITY_SIZE)
                y = random.randrange(0, settings.CITY_SIZE)
                if city.isPassable(x, y):
                    break
            zombieMachineState.m_X = x
            zombieMachineState.m_Y = y
            zombieMachineState.m_Facing = random.choice(["Up", "Right", "Down", "Left"])

            # load machine
            zombieMachineState.m_Machine = Machine()
            zombieMachineState.m_Machine.LoadMachine(file_path)

            city.zombies.append(zombieMachineState)

    def generate_humans(self, city, file_path):
        # generate humans
        assert isinstance(city, World)
        for i in range(settings.NUMBER_OF_HUMANS):
            humanMachineState = MachineState()
            humanMachineState.m_Traits = HumanTraits()
            # get a passable random location
            while True:
                x = random.randrange(0, settings.CITY_SIZE)
                y = random.randrange(0, settings.CITY_SIZE)
                if city.isPassable(x, y):
                    break
            humanMachineState.m_X = x
            humanMachineState.m_Y = y
            humanMachineState.m_Facing = random.choice(["Up", "Right", "Down", "Left"])
            humanMachineState.m_Memory = [0 for i in range(settings.HUMAN_MEMORY)]
            # load machine
            humanMachineState.m_Machine = Machine()
            humanMachineState.m_Machine.LoadMachine(file_path)

            city.humans.append(humanMachineState)

    def start(self):
        #while self.racoonCity.zombies and self.racoonCity.humans:
        while True:
            self.take_turn()
            time.sleep(1)

    def take_turn(self):
        # zombies take turn
        for zombie in self.racoonCity.zombies:
            zombie.m_Machine.TakeTurn(zombie, self.racoonCity)

        # humans take turn
        for human in self.racoonCity.humans:
            human.m_Machine.TakeTurn(human, self.racoonCity)

        self.racoonCity.month += 1

    def new_game(self, zom_path, hum_path):
        self.racoonCity.newGame()
        self.generate_zombies(self.racoonCity, zom_path)
        self.generate_humans(self.racoonCity, hum_path)


if __name__ == "__main__":
    zom = ZomFrame()
    zom.start()
    print("pause")