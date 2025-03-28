import os
import pickle
from user.loggers import Actions
from ifind.search.query import Query
import abc

class SimulatedBaseUser(object):
    """
    The simulated user. Stores references to all the required components, and contains the logical workflow for the simulation.
    """
    def __init__(self, configuration):
        self._user_context = configuration.user.user_context
        self._output_controller = configuration.output
        self._logger = configuration.user.logger
        self._action_value = Actions.START  # The action value is the action that the user has decided to perform.    
        self._logger.start_logging()
        """        
        The last_to_next_action_mapping from the last action to the next action
        decides means that after the action is peformed,
        we get a chance to update the log, state, etc.
        before performing the next action.

        When you implement the after methods, you are can define the workflow of the user.
        """
        self.last_to_next_action_mapping = {
            Actions.QUERY       : self._after_query,
            Actions.SERP        : self._after_serp,
            Actions.SNIPPET     : self._after_snippet,
            Actions.DOC         : self._after_assess_document,
            Actions.MARK        : self._after_mark,
            Actions.UTTERANCE   : self._after_utterance,
            Actions.CSRP        : self._after_csrp,
            Actions.RESPONSE    : self._after_assess_response,
            Actions.MARKRESPONSE: self._after_mark_response,
            Actions.STOP        : self._after_stop,
            Actions.START       : self._after_none,
            None                : self._after_none
        }

        """
        When an action is to be performed, the action_mapping dictionary is
        used to call the appropriate method to perform the action.
        """
        self.action_mapping = {
            Actions.QUERY  : self._do_query,
            Actions.SERP   : self._do_serp,
            Actions.SNIPPET: self._do_snippet,
            Actions.DOC    : self._do_assess_document,
            Actions.MARK   : self._do_mark_document,
            Actions.UTTERANCE: self._do_utterance,
            Actions.CSRP: self._do_csrp,
            Actions.RESPONSE: self._do_assess_response,
            Actions.MARKRESPONSE: self._do_mark_response,
            Actions.STOP: self._do_stop
        }

    def decide_action(self):
        last_action = self._user_context.get_last_action()
        self.last_to_next_action_mapping[last_action]()
    
    def _do_action(self, action):
        # Update the search context to reflect the most recent action.
        # Logging takes place within each method called (e.g. __do_query()) to reflect different values being passed.
        self._user_context.set_action(action)
        # Now call the appropriate method to perform the action.
        self._action_value = self.action_mapping[action]()
    
    def _do_query(self):
        """
        Called when the simulated user wishes to issue another query.
        This works by calling the search context for the subsequent query text, and is then issued to the search interface by the search context on behalf of the user.
        If no further queries are available, the logger is told of this - and the simulation will then stop at the next iteration.
        """
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
            
    def _do_serp(self):
        """
        Called when the simulated user wishes to examine a SERP - the "initial glance" - after issuing a query.
        If the SERP has no results, we continue with the next action - otherwise we will always go and look at said SERP.
        """
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _do_snippet(self):
        """
        Called when the user needs to make the decision whether to examine a snippet or not.
        The logic within this method supports previous observations of the same document, and whether the text within the snippet appears to be relevant.
        """
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _do_assess_document(self):
        """
        Called when a document is to be assessed.
        """
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _do_mark_document(self):
        """
        The outcome of marking a document as relevant. At this stage, the user has decided that the document is relevant; hence True can be the only result.
        """
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
        
    def _do_result_stopping_decider(self):
        """
        Method which returns whether a further snippet should be examined, the next query should be issued, or some other action.
        This is the "decision making" logic - and is abstracted to the instantiated DecisionMaker instance to work this out.
        """
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _do_utterance(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _do_csrp(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _do_assess_response(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _do_mark_response(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def do_response_stopping_decider(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _do_stop(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _after_query(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")

    def _after_serp(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")           

    def _after_snippet(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")

    def _after_assess_document(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _after_mark(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _after_none(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")

    def _after_utterance(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")

    def _after_csrp(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")

    def _after_assess_response(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _after_mark_response(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")

    def _after_stop(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")

