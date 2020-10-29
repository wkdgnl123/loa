from __future__ import annotations
from typing import Dict
import copy

from loa import utils

class Unit:    
    def __init__(self,
                 name: str = "",
                 pos: int = 0,
                 hp: int = 0,
                 att: int = 0,
                 arm: int = 0):
        # Name
        self.name = name
        
        # Position
        self.pos = pos
        
        # HP
        self.hp = hp  # Hit Points
                
        # Attack & Armor
        self.att = att  # Attack damage
        self.arm = arm  # Armor
        
    def __str__(self):
        fstr = "%s(NAME:%s,POS:%s,HP:%s,ATT:%s,ARM:%s)"
        return fstr%(self.__class__.__name__,
                     self.name,
                     self.pos,
                     self.hp,
                     self.att,
                     self.arm)
    
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        attr1 = (self.name, self.pos, self.hp, self.att, self.arm)
        attr2 = (other.name, other.pos, other.hp, other.att, other.arm)
        return attr1 == attr2
        
    def __ne__(self, other):
        attr1 = (self.name, self.pos, self.hp, self.att, self.arm)
        attr2 = (other.name, other.pos, other.hp, other.att, other.arm)
        return attr1 != attr2
    
    def __hash__(self):
        return hash(str(self))
    
    # Properties
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, val):
        utils.check_type("name", val, str)
        self._name = val
        
    @property
    def pos(self):
        return self._pos
        
    @pos.setter
    def pos(self, val):
        utils.check_nonnegative_int("pos", val)
        self._pos = val        
    
    @property
    def hp(self):
        return self._hp
        
    @hp.setter
    def hp(self, val: int):
        utils.check_nonnegative_int("hp", val)
        self._hp = val
    
    @property
    def att(self):
        return self._att
    
    @att.setter
    def att(self, val: int):
        utils.check_nonnegative_int("att", val)
        self._att = val

    @property
    def arm(self):
        return self._arm
    
    @arm.setter
    def arm(self, val: int):
        utils.check_nonnegative_int("arm", val)
        self._arm = val   

    @property
    def magics(self):
        return self._magics
    
    # Methods
    def attack(self, target: Unit):        
        utils.check_type("target", target, Unit)        
        
        target.hp = max(0, target.hp - max(1, self.att - target.arm))
        self.hp = max(0, self.hp - max(1, 0.5*target.att - self.arm))
        
        print(self.name, "attacks", target.name)
         
    def update(self, obj: Unit):
        utils.check_type("obj", obj, Unit)        
        self.name = obj.name
        self.hp = obj.hp
        self.att = obj.att
        self.arm = obj.arm
