
import logging


logger = None

def get_logger(name=None, fpath=None, level=logging.INFO):
    
    global logger
    if not logger:
        # Create logger
        logger = logging.getLogger(name)        
        
        # Formatting
        formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s",
                                      "%Y-%m-%d %H:%M:%S")        
        
        # Standard output
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        
        # File output
        if fpath:
            file_handler = logging.FileHandler(fpath)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
                
    # Set log level
    logger.setLevel(level)
    return logger


def check_nonnegative_int(varname, val):
    if not isinstance(val, int):
        raise ValueError("%s should be int type."%(varname))
        
    if val < 0:
        raise ValueError("%s cannot be negative."%(varname))

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
        raise TypeError(err_msg)
        
        
def attack(unit, target, wtype):
    check_type("unit", unit, wtype)
    check_type("target", target, wtype)        
    
    target.hp = max(0, target.hp - max(1, unit.att - target.arm))
    unit.hp = max(0, unit.hp - max(1, 0.5*target.att - unit.arm))
    
    