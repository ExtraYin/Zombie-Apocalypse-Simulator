"""
@author: Yida Yin

Copyright (c) 16/3/17 Yida Yin. All rights reserved.
"""


class ZombieTraits(object):
    ACTIONS_PER_TURN = 1
    MEMORY_LOCATIONS = 0
    INFECT_ON_ATTACK = True


class HumanTraits(object):
    ACTIONS_PER_TURN = 2
    MEMORY_LOCATIONS = 2
    INFECT_ON_ATTACK = False