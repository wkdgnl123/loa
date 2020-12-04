from __future__ import annotations
from typing import List
from os.path import join as pjoin

import yaml

from loa.unit import Unit
from loa import utils


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
    
    @property
    def name(self):
        return self._name
        
    @property
    def units(self) -> List[Unit]:
        return self._units

    @property
    def num_units(self):
        return len(self)

            
    def initialize(self):
        """Create unit instances and arrange them.        
           
           for i in range(self.num_units):
               self.units.append(UnitFactory.create(i))
        """
        pass
        #raise NotImplementedError()        

    def arrange(self, enemy: Team):
        raise NotImplementedError()
        # Implement your arrangement strategy at each turn.
              
        
class TeamExaminer:
    
    def __init__(self, fname_constraint=None):
        
        
        if not fname_constraint:
            fname_constraint = "constraint_round-001.yml"            

        self._constraint = self._load_constraint(fname_constraint)
        
    def _load_constraint(self, fname: str):
        dpath_constraint = pjoin(utils.get_package_path(), "constraints")
        fpath_constraint = pjoin(dpath_constraint, fname)
        
                
        with open(fpath_constraint, "rt") as fin:
            return yaml.safe_load(fin.read())        
    
    def check(self, team: Team):
        self._check_types(team)
        self._check_positions(team)
        self._check_constraints(team)
        
    
    def _check_types(self, team: Team):
        utils.check_type("team", team, Team)        
        for unit in team:
            if not isinstance(unit, Unit):
                err_msg = "An element of Team should be Unit type, "\
                          "not %s"%(type(unit))
                raise TypeError(err_msg)
                
    def _check_positions(self, team: Team):
        for i, unit in enumerate(team):
            if unit.pos != i:
                err_msg = "[%s] The position of the unit " \
                          "is different from the real position %d (not %d)."
                raise ValueError(err_msg%(unit.pos, i))
        
    def _check_constraints(self, team: Team):
        constraint = self._constraint
        
        CONS_TEAM = constraint['TEAM']
        CONS_NUM_UNITS = CONS_TEAM['NUM_UNITS']
        CONS_MAX_EVS = CONS_TEAM['MAX_EVS']
        # CONS_SUM_HP = CONS_TEAM['SUM_HP']
        CONS_SUM_HP_ATT_ARM = CONS_TEAM['SUM_HP_ATT_ARM']
        CONS_SUM_EVS_DIV_ARM = CONS_TEAM['SUM_EVS_DIV_ARM']
        
        
        if len(team) != CONS_NUM_UNITS:
            err_msg = "The number of units in a team should be" \
                      " %d, not %d"%(CONS_NUM_UNITS, len(team))
            raise ValueError(err_msg)
        
        sum_hp = 0
        sum_att = 0
        sum_arm = 0
        sum_evs_div_arm = 0
        for unit in team:
            if unit.evs > CONS_MAX_EVS:
                err_msg = "[%s] The evs of each unit should be " \
                          "less than or equal to %d, not %d!"
                raise ValueError(err_msg%(unit.name,
                                          CONS_MAX_EVS,
                                          unit.evs))
            
            sum_hp += unit.hp
            sum_att += unit.att
            sum_arm += unit.arm
            sum_evs_div_arm += (float(unit.evs) / float(unit.arm))
        # end of for
        
        # if sum_hp > CONS_SUM_HP:
        #     err_msg = "The summation of HP of all units in a team should be " \
        #               "less than or equal to %d, not %d!"%(CONS_SUM_HP, sum_hp)
        #     raise ValueError(err_msg)
        
        sum_hp_att_arm = sum_hp + sum_att + sum_arm
        if sum_hp_att_arm  > CONS_SUM_HP_ATT_ARM:
            err_msg = "[%s] The summation of HP, ATT, and ARM of all units in a team " \
                      "should be less than or equal to %d, not %d!"
            raise ValueError(err_msg%(team.name,
                                      CONS_SUM_HP_ATT_ARM,
                                      sum_hp_att_arm))
            
        if sum_evs_div_arm  > CONS_SUM_EVS_DIV_ARM:
            err_msg = "[%s] The summation of EVS/ARM of all units " \
                      "in a team should be less than or equal to %d, not %d!"
            raise ValueError(err_msg%(team.name,
                                      CONS_SUM_EVS_DIV_ARM,
                                      sum_evs_div_arm))
        
        
            
        
        