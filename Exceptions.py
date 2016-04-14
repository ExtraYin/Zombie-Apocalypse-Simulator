"""
Created on #DATA
@author: Yida Yin
"""


class InvalidOp(Exception):
    def __init__(self):
        self.what = "Invalid OP code or parameters."


class AccessViolation(Exception):
    def __init__(self):
        self.what = "Machine tried to access outside available memory."


class MemoryViolation(Exception):
    def __init__(self):
        self.what = "Zombie tries to access memory."


class RangedViolation(Exception):
    def __init__(self):
        self.what = "Zombie tries to do ranged attack."