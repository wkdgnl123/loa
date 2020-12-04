import copy
from typing import List
import logging

from loa.unit import Unit
from loa.team import Team
from loa.team import TeamExaminer
from loa.simulator import Simulator
from loa import utils


# import logging

# logger = logging.getLogger("SIMULATION-TEST")
# logger.setLevel(logging.INFO)

# stream_handler = logging.StreamHandler()
# logger.addHandler(stream_handler)


class MyUnit1(Unit):
    
    HP = 9  # Hit Points (health points)    
    ATT = 6  # Attack
    ARM = 5  # Armor
    EVS = 10 # Evasion
        
    def __init__(self, name, pos):
        cls = __class__
        super().__init__(name,
                         pos,
                         hp=cls.HP,
                         att=cls.ATT,
                         arm=cls.ARM,
                         evs=cls.EVS)

class MyUnit2(Unit):
    
    HP = 9  # Hit Points (health points)    
    ATT = 7  # Attack
    ARM = 4  # Armor
    EVS = 8  # Evasion
        
    def __init__(self, name, pos):
        cls = __class__
        super().__init__(name,
                         pos,
                         hp=cls.HP,
                         att=cls.ATT,
                         arm=cls.ARM,
                         evs=cls.EVS)

class MyTeam1(Team):
    def initialize(self):
        for i in range(10):
            unit = MyUnit1("[Team#1]MyUnit#%d"%(i+1), i)
            self.units.append(unit)
            
    def arrange(self, enemy: Team):        
        pass
    
class MyTeam2(Team):
    def initialize(self):
        for i in range(10):
            unit = MyUnit2("[Team#2]MyUnit#%d"%(i+1), i)
            self.units.append(unit)
            
    def arrange(self, enemy: Team):        
        pass

    
if __name__ == "__main__":
   
    simulator = Simulator()
    team1 = MyTeam1("Team#1")
    team2 = MyTeam2("Team#2")
    
    examiner = TeamExaminer()
    examiner.check(team1)
    examiner.check(team2)
    
    
    print(team1)
    print(team2)
    n_team1, n_team2, n_draws = simulator.play(team1, team2, 20, 10)
    print("Number of Team1 wins:", n_team1)
    print("Number of Team2 wins:", n_team2)
    print("Number of draws:", n_draws)
    
    if n_team1 > n_team2:
        print("Team #1 wins!")
    elif n_team1 < n_team2:
        print("Team #2 wins!")        
    else:
        print("Two teams draw...")
        