from __future__ import annotations

from typing import List
from unit import Unit

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
    
    def __init__(self):
        pass
    
    def check(self, team: Team):
        utils.check_type("team", team, Team)
        
        for unit in team:
            if isinstance(unit, Unit):
                err_msg = "An element of Team should be Unit type, "\
                          "not %s"%(type(unit))
                raise TypeError(err_msg)
    
    

        