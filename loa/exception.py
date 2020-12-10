

class TeamConsistencyError(Exception):
    
    def __init__(self, team, message=None):
        self._team = team
        self._message = message
        super().__init__(self._message)
        