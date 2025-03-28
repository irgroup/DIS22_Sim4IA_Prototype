import random
from simiir.user.loggers import Actions
from simiir.user.result_stopping_decider.base import BaseDecisionMaker

class RandomDecisionMaker(BaseDecisionMaker):
    """
    A concrete implementation of a decision maker.
    Given a probability, returns True or False from decide() dependent upon that probability.
    """
    def __init__(self, user_context, logger):
        super(RandomDecisionMaker, self).__init__(user_context, logger)
        self.__probability = 0.25
    
    def decide(self):
        """
        Returns the examine snippet or issue query actions depending on the specified probability.
        """
        if random.random() > self.__probability:
            return Actions.SNIPPET
        
        return Actions.QUERY