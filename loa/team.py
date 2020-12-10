from __future__ import annotations
from typing import List
from os.path import join as pjoin
import copy

import yaml

from loa import utils
from loa.unit import Unit
from loa.logging import write_log
from loa.exception import TeamConsistencyError

class Team:
    def __init__(self,
                 name: str,
                 units: List[Unit] = None):
        
        utils.check_type("name", name, str)
        self._name = name
        
        if units:
            utils.check_type("units", units, list)
            if len(units) != 0:
                utils.check_type("units[0]", units[0], Unit)
        else:
            units = []
            
        self._units = units
        self.initialize()
        
        
        
    def __str__(self):
        str_units = "\n".join([str(elem) for elem in self._units])
        fstr = "[%s(%s)]\n%s"
        return fstr%(self.__class__.__name__,
                     self.name,
                     str_units)
    
    
    def __repr__(self):
        return str(self)
    
    def __len__(self):
        return len(list(filter(lambda x: x, self._units)))
    
    def __getitem__(self, i):
        return self._units[i]
    
    def __setitem__(self, i, obj):
        self._units[i] = obj
        
    def __eq__(self, other: Team):        
        set_team1 = set(self.units)
        set_team2 = set(self.units)
        
        return set_team1 == set_team2
            

    def __ne__(self, other: Team):        
        return not self.__eq__(other)
        
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, val):
        utils.check_type("name", val, str)
        self._name = val
        
    @property
    def units(self) -> List[Unit]:
        return self._units

    @property
    def num_positions(self):
        return len(self._units)

    @property
    def num_units(self):
        return len(self)

            
    def initialize(self):
        """Create unit instances and arrange them.        
           
           for i in range(10):
               self.units.append(self, "MyUnit", i)
        """
        pass

    def arrange(self, enemy: Team):
        raise NotImplementedError()
        # Implement your arrangement strategy at each turn.
              
        
class TeamExaminer:
    
    def __init__(self, fname_constraints=None):
                        
        if not fname_constraints:
            fname_constraints = "constraints.yml"
            
        self._constraints = self._load_constraint(fname_constraints)
        
    def _load_constraint(self, fname: str):
        dpath_constraint = pjoin(utils.get_package_path(), "constraints")
        fpath_constraint = pjoin(dpath_constraint, fname)
        
                
        with open(fpath_constraint, "rt") as fin:
            return yaml.safe_load(fin.read())        
    
    def check(self, team: Team, league_round: str = None):
        self._check_types(team)
        self._check_positions(team)
        self._check_constraints(team, league_round)
        self._check_arrange(team, copy.deepcopy(team))
    
    def check_play(self,
                   offense: Team,
                   defense: Team,
                   league_round: str = None):
        self._check_positions(offense)        
        self._check_positions(defense)
        self._check_arrange(offense, defense)
        
    def _check_types(self, team: Team):
        utils.check_type("team", team, Team)        
        for unit in team:
            if not isinstance(unit, Unit):
                err_msg = "An element of Team should be Unit type, "\
                          "not %s"%(type(unit))
                raise TypeError(err_msg)
                
    def _check_positions(self, team: Team):
        for i, unit in enumerate(team):
            if unit and unit.pos != i:
                err_msg = "[%s] The position of the unit " \
                          "is different from the real position %d, not %d."
                raise ValueError(err_msg%(team.name, i, unit.pos))
        
    def _check_unit_uniqueness(self, team: Team):
                
        set_ids = set([id(unit) for unit in team])
                
        if len(set_ids) != len(team):
            err_msg = "Each unit in the team %s should be unique! " \
                      "%s includes redundant unit instances."%(team.name,
                                                               team.name)
            write_log(err_msg)
            raise RuntimeError(err_msg)
        
    def _check_constraints(self, team: Team, league_round=None):
        constraints = self._constraints
        
        if not league_round:
            league_round = "round-01"
            
        league_round = league_round.upper()
        if league_round == "ROUND-01":
            CONS_TEAM = constraints[league_round]['TEAM']
            CONS_NUM_UNITS = CONS_TEAM['NUM_UNITS']
            CONS_MAX_EVS = CONS_TEAM['MAX_EVS']
            CONS_SUM_HP_ATT_ARM = CONS_TEAM['SUM_HP_ATT_ARM']
            CONS_SUM_EVS_DIV_ARM = CONS_TEAM['SUM_EVS_DIV_ARM']
            
            
            if len(team) != CONS_NUM_UNITS:
                err_msg = "[%s] The number of units should be" \
                          " %d, not %d"%(team.name, CONS_NUM_UNITS, len(team))
                write_log(err_msg)
                raise ValueError(err_msg)
            
            sum_hp = 0
            sum_att = 0
            sum_arm = 0
            sum_evs_div_arm = 0
            for unit in team:
                if unit.evs > CONS_MAX_EVS:
                    err_msg = "[%s] The evs of each unit should be " \
                              "less than or equal to %.2f, not %.2f!"% \
                              (
                                  unit.name,
                                  CONS_MAX_EVS,
                                  unit.evs
                              )
                    write_log(err_msg)
                    raise ValueError(err_msg)
                # end of if
                sum_hp += unit.hp
                sum_att += unit.att
                sum_arm += unit.arm
                sum_evs_div_arm += (float(unit.evs) / float(unit.arm))
            # end of for

            sum_hp_att_arm = sum_hp + sum_att + sum_arm
            if sum_hp_att_arm  > CONS_SUM_HP_ATT_ARM:
                err_msg = "[%s] The summation of HP, ATT, and ARM " \
                          "of all units in a team should be less than " \
                          "or equal to %.2f, not %.2f!"% \
                          (
                              team.name,
                              CONS_SUM_HP_ATT_ARM,
                              sum_hp_att_arm
                          )
                write_log(err_msg)
                raise ValueError(err_msg)
                
            if sum_evs_div_arm  > CONS_SUM_EVS_DIV_ARM:
                err_msg = "[%s] The summation of EVS/ARM of all units " \
                          "in a team should be less than or " \
                          "equal to %.2f, not %.2f!"% \
                          (
                              team.name,
                              CONS_SUM_EVS_DIV_ARM,
                              sum_evs_div_arm
                          )
                write_log(err_msg)
                raise ValueError(err_msg)
            
        else:
            err_msg = "league_round=%s is not defined!"%(league_round)
            write_log(err_msg)
            raise ValueError(err_msg)
                
            
    def _check_arrange(self,
                       offense: Team,
                       defense: Team):
        
        offense_cpy = copy.deepcopy(offense)
        defense_cpy = copy.deepcopy(defense)
        offense_cpy.arrange(defense_cpy)
        self._check_consistency(offense,
                                offense_cpy,
                                "arrangement")
    
    
    def _check_consistency(self,
                           origin: Team,
                           copied: Team,
                           situation: str):
          
        if len(origin) != len(copied):
            err_msg = "The size of the team %s " \
                      "has been changed in %s!"%(origin.name, situation)
            write_log(err_msg)
            raise TeamConsistencyError(origin, err_msg)
            
    
        if origin != copied:
            err_msg = "The units in the team %s " \
                      "has been changed in %s!"%(origin.name, situation)
            write_log(err_msg)
            raise TeamConsistencyError(origin, err_msg) 
                
        
    