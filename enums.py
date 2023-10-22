from enum import Enum
from numpy import random

class Team(Enum):
    white = 0
    black = 1
    na = -1
    
    @classmethod
    def pick(cls):
        if random.rand() > 0.5:
            return cls.white
        return cls.black
    
    def change(self):
        if self == self.white:
            return self.black
        return self.white