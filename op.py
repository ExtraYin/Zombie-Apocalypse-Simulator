# coding=utf-8
"""
@author: Yida Yin

Copyright (c) 16/3/17 Yida Yin. All rights reserved.
"""

import machine
import world
from Exceptions import *
from settings import *
from traits import *
import random


class Op(object):
    def __init__(self, name, parameter):
        self.m_OpName = name
        self.m_Param = parameter

    def Execute(self, state, city=None):
        pass


# Defines the rotate operation
# Param of 0 means rotate clockwise
# Param of 1 means rotate counter-clockwise
class OpRotate(Op):
    def __init__(self, parameter):
        super(OpRotate, self).__init__("OpRotate", parameter)

    def Execute(self, state, city=None):
        assert(isinstance(state, machine.MachineState))
        if state.m_Facing == "Up":
            if self.m_Param == 0:
                state.m_Facing = "Right"
            else:
                state.m_Facing = "Left"
        elif state.m_Facing == "Right":
            if self.m_Param == 0:
                state.m_Facing = "Down"
            else:
                state.m_Facing = "Up"
        elif state.m_Facing == "Down":
            if self.m_Param == 0:
                state.m_Facing = "Left"
            else:
                state.m_Facing = "Right"
        elif state.m_Facing == "Left":
            if self.m_Param == 0:
                state.m_Facing = "Up"
            else:
                state.m_Facing = "Down"

        # Increment no matter result
        state.m_ProgramCounter += 1
        state.m_ActionsTaken += 1


# Defines the Forward operation
class OpForward(Op):
    def __init__(self, parameter):
        super(OpForward, self).__init__("OpForward", parameter)

    def Execute(self, state, city=None):
        assert(isinstance(city, world.World))
        if state.m_Facing == "Up":
            if city.isPassable(state.m_X, state.m_Y-1):
                state.m_Y -= 1
        elif state.m_Facing == "Right":
            if city.isPassable(state.m_X+1, state.m_Y):
                state.m_X += 1
        elif state.m_Facing == "Down":
            if city.isPassable(state.m_X, state.m_Y+1):
                state.m_Y += 1
        elif state.m_Facing == "Left":
            if city.isPassable(state.m_X-1, state.m_Y):
                state.m_X -= 1

        # Increment no matter result
        state.m_ProgramCounter += 1
        state.m_ActionsTaken += 1


# Defines the goto operation
# Parameter determines the line number
class OpGoto(Op):
    def __init__(self, parameter):
        super(OpGoto, self).__init__("OpGoto", parameter)

    def Execute(self, state, city=None):
        if self.m_Param > 1000:    # FIXME
            raise AccessViolation()
        state.m_ProgramCounter = self.m_Param


# Defines the je operation
# Parameter determines the line number
class OpJe(Op):
    def __init__(self, parameter):
        super(OpJe, self).__init__("OpJe", parameter)

    def Execute(self, state, city=None):
        if self.m_Param > 1000:  # FIXME
            raise AccessViolation()
        if state.m_Test:
            state.m_ProgramCounter = self.m_Param
        else:
            state.m_ProgramCounter += 1


# Exactly like je, but jumps if the flag is false.
class OpJne(Op):
    def __init__(self, parameter):
        super(OpJne, self).__init__("OpJne", parameter)

    def Execute(self, state, city=None):
        if self.m_Param > 1000:   # FIXME
            raise AccessViolation()
        if not state.m_Test:
            state.m_ProgramCounter = self.m_Param
        else:
            state.m_ProgramCounter += 1


# Set test flag to true if facing a wall.
class OpTestWall(Op):
    def __init__(self, parameter):
        super(OpTestWall, self).__init__("OpTestWall", parameter)

    def Execute(self, state, city=None):
        if state.m_Facing == "Up":
            state.m_Test = (state.m_Y == 0)
        if state.m_Facing == "Left":
            state.m_Test = (state.m_X == 0)
        if state.m_Facing == "Right":
            state.m_Test = (state.m_Y == CITY_SIZE-1)
        if state.m_Facing == "Down":
            state.m_Test = (state.m_Y == CITY_SIZE-1)

        state.m_ProgramCounter += 1


# Randomly set test flag to true or false.
class OpTestRandom(Op):
    def __init__(self, parameter):
        super(OpTestRandom, self).__init__("OpTestRandom", parameter)

    def Execute(self, state, city=None):
        state.m_Test = random.choice([0, 1])

        state.m_ProgramCounter += 1


# Set test flag to true if a zombie is n tiles in front, where n can be either 1 or 2.
class OpTestZombie(Op):
    def __init__(self, parameter):
        super(OpTestZombie, self).__init__("OpTestZombie", parameter)

    def Execute(self, state, city=None):
        assert(isinstance(city, world.World))
        if state.m_Facing == "Up":
            state.m_Test = city.isZombie(state.m_X, state.m_Y-self.m_Param)
        if state.m_Facing == "Right":
            state.m_Test = city.isZombie(state.m_X+self.m_Param, state.m_Y)
        if state.m_Facing == "Down":
            state.m_Test = city.isZombie(state.m_X, state.m_Y+self.m_Param)
        if state.m_Facing == "Left":
            state.m_Test = city.isZombie(state.m_X-self.m_Param, state.m_Y)

        state.m_ProgramCounter += 1


# Set test flag to true if a human is n tiles in front, where n can be either 1 or 2.
class OpTestHuman(Op):
    def __init__(self, parameter):
        super(OpTestHuman, self).__init__("OpTestHuman", parameter)

    def Execute(self, state, city=None):
        assert(isinstance(city, world.World))
        if state.m_Facing == "Up":
            state.m_Test = city.isHuman(state.m_X, state.m_Y-self.m_Param)
        if state.m_Facing == "Right":
            state.m_Test = city.isHuman(state.m_X+self.m_Param, state.m_Y)
        if state.m_Facing == "Down":
            state.m_Test = city.isHuman(state.m_X, state.m_Y+self.m_Param)
        if state.m_Facing == "Left":
            state.m_Test = city.isHuman(state.m_X-self.m_Param, state.m_Y)

        state.m_ProgramCounter += 1


# Set test flag to true if facing an open tile.
class OpTestPassable(Op):
    def __init__(self, parameter):
        super(OpTestPassable, self).__init__("OpTestPassable", parameter)

    def Execute(self, state, city=None):
        assert(isinstance(city, world.World))
        assert (isinstance(state, machine.MachineState))
        if state.m_Facing == "Up":
            state.m_Test = city.isPassable(state.m_X, state.m_Y-1)
        if state.m_Facing == "Right":
            state.m_Test = city.isPassable(state.m_X+1, state.m_Y)
        if state.m_Facing == "Down":
            state.m_Test = city.isPassable(state.m_X, state.m_Y+1)
        if state.m_Facing == "Left":
            state.m_Test = city.isPassable(state.m_X-1, state.m_Y)

        state.m_ProgramCounter += 1



# Try to kill whatever is right in front of you. If a zombie attacks a human, the human becomes a zombie.
# If a human attacks a zombie, the zombie dies. If a zombie attacks a zombie, nothing happens.
# If a human attacks a human, the human being attacked dies.
# If you try to attack a wall or there’s nothing in front, it just wastes the action.
class OpAttack(Op):
    def __init__(self, parameter):
        super(OpAttack, self).__init__("OpAttack", parameter)

    def Execute(self, state, city=None):
        assert(isinstance(city, world.World))
        assert(isinstance(state, machine.MachineState))
        if state.m_Facing == "Up":
            city.attack(state.m_X, state.m_Y-1, state.m_Traits.INFECT_ON_ATTACK, state)
        if state.m_Facing == "Right":
            city.attack(state.m_X+1, state.m_Y, state.m_Traits.INFECT_ON_ATTACK, state)
        if state.m_Facing == "Down":
            city.attack(state.m_X, state.m_Y+1, state.m_Traits.INFECT_ON_ATTACK, state)
        if state.m_Facing == "Left":
            city.attack(state.m_X-1, state.m_Y, state.m_Traits.INFECT_ON_ATTACK, state)

        state.m_ProgramCounter += 1
        state.m_ActionsTaken += 1


# Attack two tiles in front of you with a ranged attack.
# Only humans can use a ranged attack.Whatever a human attacks dies.
# If there’s nothing to attack there, it wastes the action.Throws an exception if called from a zombie.
class OpRangedAttack(Op):
    def __init__(self, parameter):
        super(OpRangedAttack, self).__init__("OpRangedAttack", parameter)

    def Execute(self, state, city=None):
        assert(isinstance(city, world.World))
        assert(isinstance(state, machine.MachineState))
        if state.m_Traits.INFECT_ON_ATTACK:
            raise RangedViolation

        if state.m_Facing == "Up":
            city.attack(state.m_X, state.m_Y-2, state.m_Traits.INFECT_ON_ATTACK, state)
        if state.m_Facing == "Right":
            city.attack(state.m_X+2, state.m_Y, state.m_Traits.INFECT_ON_ATTACK, state)
        if state.m_Facing == "Down":
            city.attack(state.m_X, state.m_Y+2, state.m_Traits.INFECT_ON_ATTACK, state)
        if state.m_Facing == "Left":
            city.attack(state.m_X-2, state.m_Y, state.m_Traits.INFECT_ON_ATTACK, state)

        state.m_ProgramCounter += 1
        state.m_ActionsTaken += 1


# Automatically ends the turn, even if there are more actions left.
class OpEndTurn(Op):
    def __init__(self, parameter):
        super(OpEndTurn, self).__init__("OpEndTurn", parameter)

    def Execute(self, state, city=None):
        state.m_ProgramCounter += 1
        state.m_ActionsTaken += 1

# Set the current memory slot to memory slot n.
# Throws exception if memory slot n is invalid or attempted by zombie.
class OpMem(Op):
    def __init__(self, parameter):
        super(OpMem, self).__init__("OpMem", parameter)

    def Execute(self, state, city=None):
        if isinstance(state.m_Traits, ZombieTraits):
            # test if zombie
            raise MemoryViolation
        if self.m_Param >= HUMAN_MEMORY or self.m_Param < 0:
            # throw if out of range
            raise MemoryViolation
        state.m_Slot = self.m_Param
        state.m_ProgramCounter += 1


# Write the value n to the current memory slot.
# Throws exception if there is no current memory slot or attempted by zombie.
class OpSet(Op):
    def __init__(self, parameter):
        super(OpSet, self).__init__("OpSet", parameter)

    def Execute(self, state, city=None):
        if isinstance(state.m_Traits, ZombieTraits):
            # test if zombie
            raise MemoryViolation
        if state.m_Slot < 0 or state.m_Slot >= HUMAN_MEMORY:
            # throw if out of range
            raise MemoryViolation
        state.m_Memory[state.m_Slot] = self.m_Param

        state.m_ProgramCounter += 1



# Increment the value in the current memory slot by 1.
# Throws exception if there is no current memory slot or attempted by zombie.
class OpInc(Op):
    def __init__(self, parameter):
        super(OpInc, self).__init__("OpInc", parameter)

    def Execute(self, state, city=None):
        if isinstance(state.m_Traits, ZombieTraits):
            # test if zombie
            raise MemoryViolation
        if state.m_Slot < 0 or state.m_Slot >= HUMAN_MEMORY:
            # throw if out of range
            raise MemoryViolation
        state.m_Memory[state.m_Slot] += 1

        state.m_ProgramCounter += 1


# Decrement the value in the current memory slot by 1.
# Throws exception if there is no current memory slot or attempted by zombie.
class OpDec(Op):
    def __init__(self, parameter):
        super(OpDec, self).__init__("OpDec", parameter)

    def Execute(self, state, city=None):
        if isinstance(state.m_Traits, ZombieTraits):
            # test if zombie
            raise MemoryViolation
        if state.m_Slot < 0 or state.m_Slot >= HUMAN_MEMORY:
            # throw if out of range
            raise MemoryViolation
        state.m_Memory[state.m_Slot] -= 1

        state.m_ProgramCounter += 1



# Set the test flag to true if the value in the current memory slot equals n.
# Throws exception if there is no current memory slot or attempted by zombie.
class OpTestMem(Op):
    def __init__(self, parameter):
        super(OpTestMem, self).__init__("OpTestMem", parameter)

    def Execute(self, state, city=None):
        if isinstance(state.m_Traits, ZombieTraits):
            # test if zombie
            raise MemoryViolation
        if state.m_Slot < 0 or state.m_Slot >= HUMAN_MEMORY:
            # throw if out of range
            raise MemoryViolation
        state.m_Test = (state.m_Memory[state.m_Slot] == self.m_Param)

        state.m_ProgramCounter += 1



# Saves the coordinates of the current x coordinate into mem slot 0, and current y coordinate into mem slot 1.
# Throws an exception if attempted by a zombie.
class OpSaveLoc(Op):
    def __init__(self, parameter):
        super(OpSaveLoc, self).__init__("OpSaveLoc", parameter)

    def Execute(self, state, city=None):
        if isinstance(state.m_Traits, ZombieTraits):
            # test if zombie
            raise MemoryViolation
        if state.m_Slot < 0 or state.m_Slot >= HUMAN_MEMORY:
            # throw if out of range
            raise MemoryViolation
        state.m_Memory[0] = state.m_X
        state.m_Memory[1] = state.m_Y

        state.m_ProgramCounter += 1
