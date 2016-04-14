"""
@author: Yida Yin

Copyright (c) 16/3/17 Yida Yin. All rights reserved.
"""
from op import *
from Exceptions import *

class Facing(object):
    # TODO: making Facing a structure
    Up = 0
    Right = 1
    Down = 2
    Left = 3

class MachineState(object):
    def __init__(self):
        self.m_ProgramCounter = 1
        self.m_ActionsTaken = 0
        self.m_Facing = "UP"  # Up, Right, Down, Left
        self.m_X = 0
        self.m_Y = 0
        self.m_Test = False
        self.m_Memory = None
        self.m_Slot = -100

        self.m_Traits = None
        self.m_Machine = Machine()


class Machine(object):
    def __init__(self):
        self.name = ""
        self.m_Ops = []

    def LoadMachine(self, file_path):
        with open(file_path, 'r') as f:
            for line in f:
                # get rid of comments
                if line.find(";") != -1:
                    line = line[:line.find(";")]
                line = line.replace(" ", "")
                line = line.replace("\n", "")
                line = line.replace("\t", "")

                # get op name and parameter
                if line.find(",") != -1:
                    opName = line[:line.find(",")]
                    param = int(line[line.find(",") + 1:])
                else:
                    opName = line
                    param = -1
                # print opName, param
                # generate op sequence
                if opName == "rotate":
                    if param != 0 and param != 1:
                        raise InvalidOp()
                    self.m_Ops.append(OpRotate(param))
                elif opName == "forward":
                    if param != -1:
                        raise InvalidOp()
                    self.m_Ops.append(OpForward(param))
                elif opName == "goto":
                    if param <= 0:
                        raise InvalidOp()
                    self.m_Ops.append(OpGoto(param))
                elif opName == "je":
                    if param <= 0:
                        raise InvalidOp()
                    self.m_Ops.append(OpJe(param))
                elif opName == "jne":
                    if param <= 0:
                        raise InvalidOp()
                    self.m_Ops.append(OpJne(param))
                elif opName == "test_wall":
                    if param != -1:
                        raise InvalidOp()
                    self.m_Ops.append(OpTestWall(param))
                elif opName == "test_random":
                    if param != -1:
                        raise InvalidOp()
                    self.m_Ops.append(OpTestRandom(param))
                elif opName == "test_zombie":
                    if param != 1 and param != 2:
                        raise InvalidOp()
                    self.m_Ops.append(OpTestZombie(param))
                elif opName == "test_human":
                    if param != 1 and param != 2:
                        raise InvalidOp()
                    self.m_Ops.append(OpTestHuman(param))
                elif opName == "test_passable":
                    if param != -1:
                        raise InvalidOp()
                    self.m_Ops.append(OpTestPassable(param))
                elif opName == "attack":
                    if param != -1:
                        raise InvalidOp()
                    self.m_Ops.append(OpAttack(param))
                elif opName == "ranged_attack":
                    if param != -1:
                        raise InvalidOp()
                    self.m_Ops.append(OpRangedAttack(param))
                elif opName == "endturn":
                    if param != -1:
                        raise InvalidOp()
                    self.m_Ops.append(OpEndTurn(param))
                elif opName == "mem":
                    if param < 0:
                        raise InvalidOp()
                    self.m_Ops.append(OpMem(param))
                elif opName == "set":
                    if param < 0:
                        raise InvalidOp()
                    self.m_Ops.append(OpSet(param))
                elif opName == "inc":
                    if param != -1:
                        raise InvalidOp()
                    self.m_Ops.append(OpInc(param))
                elif opName == "dec":
                    if param != -1:
                        raise InvalidOp()
                    self.m_Ops.append(OpDec(param))
                elif opName == "test_mem":
                    if param < 0:
                        raise InvalidOp()
                    self.m_Ops.append(OpTestMem(param))
                elif opName == "save_loc":
                    if param != -1:
                        raise InvalidOp()
                    self.m_Ops.append(OpSaveLoc(param))
                else:
                    raise InvalidOp()

    def Reload(self):
        self.name = ""
        self.m_Ops = []

    def TakeTurn(self, state, city):
        assert (isinstance(state, MachineState))
        state.m_ActionsTaken = 0
        while state.m_ActionsTaken < state.m_Traits.ACTIONS_PER_TURN:
            try:  # dirty fix!!
                self.m_Ops[state.m_ProgramCounter - 1].Execute(state, city)
            except IndexError:
                state.m_ProgramCounter = 1
                self.m_Ops[state.m_ProgramCounter - 1].Execute(state, city)
