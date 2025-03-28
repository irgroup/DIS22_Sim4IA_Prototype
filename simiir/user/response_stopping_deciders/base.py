import abc
import random
from simiir.user.loggers import Actions

class BaseResponseDecisionMaker(object):
    """
    
    """
    def __init__(self, user_context, logger):
        self._user_context = user_context
        self._logger = logger
    
    
    def decide(self):
        """
        Abstract method - must be implemented by an inheriting class.
        Returns an action - from the loggers.Actions enum.
        """
        
        # randomly decide whether to continue or not, for now
        action = Actions.STOP
        if random.random() < 0.5:
            action = Actions.UTTERANCE

        return action