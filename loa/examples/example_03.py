import unittest
from loa.unit import Unit
from loa.team import Team
from loa.team import TeamExaminer
from loa.judge import EachTurnMaxSurvivalJudge
from loa.simulator import BasicSimulator
from loa.logging import use_logging, finish_logging


class MyUnit1(Unit):
    
    HP = 20  # Hit Points (health points)    
    ATT = 14 # Attack
    ARM = 8  # Armor
    EVS = 0  # Evasion
        
    def __init__(self, team, name, pos):
        cls = __class__
        super().__init__(team,
                         name,
                         pos,
                         hp=cls.HP,
                         att=cls.ATT,
                         arm=cls.ARM,
                         evs=cls.EVS)

class MyUnit2(Unit):
    
    HP = 21  # Hit Points (health points)    
    ATT = 14  # Attack
    ARM = 10 # Armor
    EVS = 0  # Evasion
        
    def __init__(self, team, name, pos):
        cls = __class__
        super().__init__(team,
                         name,
                         pos,
                         hp=cls.HP,
                         att=cls.ATT,
                         arm=cls.ARM,
                         evs=cls.EVS)

class MyTeam(Team):
    def initialize(self):
        for i in range(10):
            unit = MyUnit1(self, "A-Unit%02d"%(i+1), i)
            self.units.append(unit)
            
    def arrange(self, enemy: Team):        
        pass
    
class MyTeam2(Team):
    def initialize(self):
        for i in range(10):
            unit = MyUnit2(self, "B-Unit%02d"%(i+1), i)
            self.units.append(unit)
            
    def arrange(self, enemy: Team):
        first_unit = self.units[0]
        for i in range(self.num_positions - 1):
            j = i + 1 
            self.units[i] = self.units[j]
            if self.units[i] != None:
               self.units[i].pos = i 
        # end of for
        self.units[-1] = first_unit
        if self.units[-1] != None:
            self.units[-1].pos = self.num_positions - 1

    
if __name__ == "__main__":
    unittest.main()
        
