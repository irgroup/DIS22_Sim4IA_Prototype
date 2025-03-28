import os
import pickle
from user.loggers import Actions
from ifind.search.query import Query
from sims.base import SimulatedBaseUser

class SimulatedConversationalUser(SimulatedBaseUser):
    """
    The simulated user. Stores references to all the required components, and contains the logical workflow for the simulation.
    """
    def __init__(self, configuration):
        # call the parent class constructor
        super(SimulatedConversationalUser, self).__init__(configuration)

        self._utterance_generator = configuration.user.utterance_generator
        self._csrp_impression = configuration.user.csrp_impression
        self._response_classifier = configuration.user.response_classifier
        self._response_stopping_decision_maker = configuration.user.response_decision_maker

        """
        The simple workflow implemented below is as follows. Steps with asterisks are DECISION POINTS.

        (1)  User issues an Utterance
        (2)  User looks at the Conversational Search Result Page (CSRP)
        (3*) If the CSRP (and its response) is looking good or not too long
            goto (4)(examine response), else (1) interrupt the conversation, and issue another utterance
         
        (4)  Examine Response
        (5*) If the response is relevant, goto (6) else decide whether to goto (1) or stop.
        (6)  Mark the response as relevant
        (7*) Decide whether to goto (1) or stop.
        """
    
    def _do_utterance(self):
        """
        Called when the simulated user wishes to issue an utterance.
        """
        self._utterance_generator.update_model(self._user_context)
        # Get a query from the generator.
        utterance_text = self._utterance_generator.get_next_utterance(self._user_context)
        
        if utterance_text:
            self._user_context.add_issued_utterance(utterance_text)  
            self._logger.log_action(Actions.UTTERANCE, utterance=utterance_text)
            # reusing the save to query log onthe output controller for utterances
            self._output_controller.log_query(utterance_text)
            return True
        
        self._output_controller.log_info(info_type="OUT_OF_UTTERANCES")
        #self._logger.utterances_exhausted()
        return False

    def _do_csrp(self):
        """
        Called when the simulated user wishes to examine a CSRP - the "initial glance" - after issuing a utterance.
        If the CSRP is taking too long or too poor, they will interpret, and issue another utterance.
        """
        #if self._user_context.get_current_response_length() == 0:
        #    self._logger.log_action(Actions.CSRP, status="EMPTY_CRP")
        #    return False  # No results present; return False (we don't continue with this SERP)
        is_csrp_attractive = self._csrp_impression.is_csrp_attractive()
        self._user_context.add_csrp_impression(is_csrp_attractive)  # Update the search context.    
        
        if is_csrp_attractive:
            self._logger.log_action(Actions.CSRP, status="EXAMINE_CSRP")
        else:
            self._logger.log_action(Actions.CSRP, status="INTERUPT_CSRP")
        
        return is_csrp_attractive
    
    def _do_assess_response(self):
        """
        Called when a response is to be assessed.
        """
        judgment = False
        if self._user_context.get_last_response():
            response = self._user_context.get_current_response()
            self._logger.log_action(Actions.RESPONSE, status="EXAMINING_RESPONSE", response=response)

            if self._response_classifier.is_relevant(response):
                response.judgment = 1
                self._user_context.add_relevant_response(response)
                judgment = True
            else:
                response.judgment = 0
                self._user_context.add_irrelevant_response(response)
                judgment = False

        self._response_classifier.update_model(self._user_context)
        
        return judgment
    
    def _do_mark_response(self):
        """
        The outcome of viewing a response as relevant. At this stage, the user has decided that the document is relevant; hence True can be the only result.
        """
        judgement_message = {0: 'CONSIDERED_NOT_RELEVANT', 1: 'CONSIDERED_RELEVANT'}
        response = self._user_context.get_current_response()
        self._logger.log_action(Actions.MARKRESPONSE, status=judgement_message[response.judgment])
        return True
    
    def _do_response_stopping_decider(self):
        """
        Decide whether to issue another utterance or stop.
        """
        out = self._response_stopping_decision_maker.decide()
        
        return out
    
    def _do_stop(self):
        """
        Called when the simulated user wishes to stop.
        """
        self._logger.log_action(Actions.STOP)
        return None


    def _after_utterance(self):
        self._do_action(Actions.CSRP)

    def _after_csrp(self):
        if self._action_value:
            self._do_action(Actions.RESPONSE)
        else:
            self._do_action(Actions.UTTERANCE)

    def _after_assess_response(self):
        if self._action_value:
            self._do_action(Actions.MARKRESPONSE)
        else:
            self._do_action(self._do_response_stopping_decider())
    
    def _after_mark_response(self):
        self._do_action(self._do_response_stopping_decider())

    def _after_stop(self):
        return None
    
    def _after_none(self):
        self._do_action(Actions.UTTERANCE)
    