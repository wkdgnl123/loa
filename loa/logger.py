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
