import abc

class BaseDecisionMaker(object):
    """
    
    """
    def __init__(self, user_context, logger):
        self._user_context = user_context
        self._logger = logger
    
    @abc.abstractmethod
    def decide(self):
        """
        Abstract method - must be implemented by an inheriting class.
        Returns an action - from the loggers.Actions enum.
        """
        pass