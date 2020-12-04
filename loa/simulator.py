import copy
import random

from loa.unit import Unit
from loa.team import Team
from loa import utils


class Simulator:    
    # def __init__(self,
    #              num_turns: int = 10,
    #              num_repeats: int = 5):
        
        # if num_turns % 2 != 0:
        #     raise ValueError("num_turns should be even number.")
            
        # self.num_turns = num_turns  # Number of turns
        # self.num_repeats = num_repeats  # Number of repeats for plays
        
    # @property
    # def num_turns(self):
    #     return self._num_turns
    
    # @num_turns.setter
    # def num_turns(self, val):
    #     utils.check_type("num_turns", val, int)
    #     self._num_turns = val
        
    # @property
    # def num_repeats(self):
    #     return self._num_repeats
    
    # @num_repeats.setter
    # def num_repeats(self, val):
    #     utils.check_type("num_repeats", val, int)
    #     self._num_repeats = val
    def __init__(self):
        pass
        
    def play(self,
             team1: Team,
             team2: Team,
             num_turns: int = 10,
             num_repeats: int =10):
        utils.check_type("team1", team1, Team)
        utils.check_type("team2", team2, Team)

        if len(team1) != len(team2):
            raise ValueError("The sizes of team1 and team2 dost not match.")
        
        num_wins_team1 = 0
        num_wins_team2 = 0
        num_draws = 0
        
        for i in range(num_repeats):            
            team1_cpy = copy.deepcopy(team1)
            team2_cpy = copy.deepcopy(team2)
            if i % 2 == 0:
                offense, defense = team1_cpy, team2_cpy
            else:
                offense, defense = team2_cpy, team1_cpy
                
            for t in range(num_turns):
                print("[Repeat #%d Turn #%d]"%(i+1, t+1))
                offense_cpy = copy.deepcopy(offense)
                defense_cpy = copy.deepcopy(defense)                
                
                # Arrange
                offense.arrange(defense_cpy)
                self._verify_consistency(offense, offense_cpy, "arragement")
                
                # Attack
                self._apply_attack(offense, defense)
                #self.check_consistency(offense, offense_cpy, "attack")
            
                self._clear_dead_units(offense)
                self._clear_dead_units(defense)
                
                # print("len(offense)", len(offense))
                # print("len(defense)", len(defense))
                
                if len(offense) == 0 or len(defense) == 0:
                    break                                        
                
                offense, defense = defense, offense
            # end of for
            
            if len(team1_cpy) > len(team2_cpy):  # Team #1 wins.
                num_wins_team1 += 1
            elif len(team1_cpy) < len(team2_cpy):
                num_wins_team2 += 1
            else:  # Draw
                num_draws += 1
        # end of for
        return num_wins_team1, num_wins_team2, num_draws

    
    def _check_evasion(self, target):
        evsr = target.evs / 100.  # Evasion Rate (EVSR)
        rn = random.uniform(0, 1)
        if rn  <= evsr:
            print(target.name, "evades with %.4f! (RN: %.4f)"%(evsr, rn))
            return True
            
        return False            
      
    def _apply_attack(self, offense: Team, defense: Team):
        for i, unit in enumerate(offense):            
            target = defense[i]
            if unit and target:
                if self._check_evasion(target):
                    continue
                
                unit_cpy = copy.deepcopy(unit)
                target_cpy = copy.deepcopy(defense[i])
                unit.attack(target)

                # Check consistency                
                utils.attack(unit_cpy, target_cpy, Unit)
                if unit_cpy != unit:
                    err_msg = "%s.attack() performs "\
                              "illegal behaviors."%(unit.__class__)
                    raise RuntimeError(err_msg)
        
        
    def _clear_dead_units(self, team: Team):
        for i, unit in enumerate(team):
            if not unit:
                continue
            
            if unit.hp <= 0:
                team[i] = None
            
    def _verify_consistency(self, obj1, obj2, situation):
        if len(obj1) != len(obj2):
            raise RuntimeError("Team size has been changed "
                               "during %s."%(situation))
            
        set1 = set([elem for elem in obj1])
        set2 = set([elem for elem in obj2])
        
        if set1 != set2:
            err_msg = "The unit of team %s " \
                      "has been changed during %s."%(obj1.name, situation)
            raise RuntimeError(err_msg)
    