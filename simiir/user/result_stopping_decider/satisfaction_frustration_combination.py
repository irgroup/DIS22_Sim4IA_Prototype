from simiir.user.loggers import Actions
from simiir.user.result_stopping_decider.base import BaseDecisionMaker
from simiir.user.result_stopping_decider.total_nonrelevant import TotalNonrelDecisionMaker
from simiir.user.result_stopping_decider.time_limited_satisfaction import TimeLimitedSatisfactionDecisionMaker

class SatisfactionFrustrationCombinationDecisionMaker(BaseDecisionMaker):
    """
    A concrete implementation of a decision maker, implementing a combination of the frustration and satisfaction heuristics.
    If one says move to the next query, then abandon the query!
    """
    def __init__(self, user_context, logger, relevant_threshold=3, nonrelevant_threshold=3, timeout_threshold=20):
        """
        Instantiates the decision maker.
        """
        super(SatisfactionFrustrationCombinationDecisionMaker, self).__init__(user_context, logger)
        self.__relevant_threshold = relevant_threshold
        self.__nonrelevant_threshold = nonrelevant_threshold
        self.__timeout_threshold = timeout_threshold
        
        self.__frustration = TotalNonrelDecisionMaker(user_context=user_context,
                                                      logger=logger,
                                                      nonrelevant_threshold=self.__nonrelevant_threshold)
        
        self.__satisfaction = TimeLimitedSatisfactionDecisionMaker(user_context=user_context,
                                                                   logger=logger,
                                                                   relevant_threshold=self.__relevant_threshold,
                                                                   timeout_threshold=self.__timeout_threshold)
    
    def decide(self):
        """
        If one says query, then the searcher will abandon the query and reformulate.
        """
        frustration_decision = self.__frustration.decide()
        satisfaction_decision = self.__satisfaction.decide()
        
        if frustration_decision == Actions.QUERY or satisfaction_decision == Actions.QUERY:
            return Actions.QUERY
        
        return Actions.SNIPPET