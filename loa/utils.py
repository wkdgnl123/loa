import os
from loa.logging import write_log

def get_current_round():
    return "ROUND-01"

def get_package_path():                
    return os.path.abspath(os.path.dirname(__file__))


def check_nonnegative_int(varname, val):
    if not isinstance(val, int):
        err_msg = "%s should be int type."%(varname)
        write_log(err_msg)
        raise ValueError(err_msg)
        
    if val < 0:
        err_msg = "%s cannot be negative."%(varname)
        write_log(err_msg)
        raise ValueError(err_msg)

def check_nonnegative_float(varname, val):
    if not isinstance(val, float) and not isinstance(val, int):
        err_msg = "%s should be float type."%(varname)
        write_log(err_msg)
        raise ValueError(err_msg)
        
    if val < 0.:
        err_msg = "%s cannot be negative."%(varname)
        write_log(err_msg)
        raise ValueError(err_msg)

def check_type(varname, obj, wtype):
    """Check object for a wanted type.

    Parameters
    ----------
    varname : str
        Variable name.
    obj : Object
        Object to be chekced.
    wtype : Type
        Wanted Type.

    Raises
    ------
    TypeError

    Returns
    -------
    None.

    """
    if not isinstance(obj, wtype):
        err_msg = "%s should be %s type, not %s"%(varname, wtype, type(obj))
        write_log(err_msg)
        raise TypeError(err_msg)
        
        
def attack(unit, target, wtype):
    check_type("unit", unit, wtype)
    check_type("target", target, wtype)        
    
    target.hp = max(0, target.hp - max(1, unit.att - target.arm))
    unit.hp = max(0, unit.hp - max(1, 0.5*target.att - unit.arm))
    
    
def check_team_consistency(obj1, obj2, situation):
    if len(obj1) != len(obj2):
        err_msg = "Team size has been changed during %s!"%(situation)
        write_log(err_msg)
        raise RuntimeError(err_msg)
        
    set1_units = set([unit for unit in obj1])
    set2_units = set([unit for unit in obj2])

    if set1_units != set2_units:
        err_msg = "The units in the team %s " \
                  "has been changed during %s!"%(obj1.name, situation)
        write_log(err_msg)
        raise RuntimeError(err_msg)