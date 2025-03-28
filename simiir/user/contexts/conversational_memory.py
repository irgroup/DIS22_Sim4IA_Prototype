import os
import abc
import logging
from simiir.user.loggers import Actions
from ifind.search.query import Query
from simiir.search.interfaces import Document
from simiir.user.contexts.memory import Memory

log = logging.getLogger('user_context.user_context')

class ConversationalMemory(Memory):
    """
    The "memory" of the simulated conversational search user.

    We are assuming that the memory of the user is perfect.

    Contains details such as the documents that have been examined by the user.
    This class also provides a 
    link between the simulated converational user and the conversationa search agent/interface -

    """
    def __init__(self, search_interface, output_controller, topic):
        """
        Several instance variables here to track the different aspects of the search process.
        """
        super(ConversationalMemory, self).__init__(search_interface, output_controller, topic)
        
        self._last_utterance = None                  # The Utterance object that was issued.
        self._last_response = None                # Response for the utterance.
        self._last_csrp_impression = None        # Response for the last Conversational SERP impression upon the searcher
        self._current_utternance = None
        self._current_response = None
        self._current_csrp_impression = None
        self._issued_utterances = []                # A list of utterances issued in chronological order.
        self._csrp_impressions = []              # A list of Conversational SERP impressions in chronological order. The length == issued_queries above.
        self._attractive_csrp_count = 0          # Count of CSRP viewed that were attractive enough to view.
        self._unattractive_csrp_count = 0        # Count of CSRP viewed that were judged to be unattractive.
        self.utterance_limit = 0                     # 0 - no limit on the number issued. Otherwise, the number of queries is capped
        self._responses_examined = []
        self._relevant_responses = []


    def report(self):
        """
        Returns basic statistics held within the search context at the time of calling.
        Ideally, call at the end of the simulation for a complete set of stats.
        """
        return_string = f"""
            Number of Utterances Issued: {len(self._issued_utterances)}
            Numbeer of Conversational SERP Impressions: {len(self._csrp_impressions)}
            Number of Responses Examined: {len(self._responses_examined)}
        """
        self._output_controller.log_info(info_type="SUMMARY")
        self._output_controller.log_info(info_type="TOTAL_UTTERANCES_ISSUED", text=len(self._issued_utterances))
        self._output_controller.log_info(info_type="TOTAL_CSRP_IMPRESSIONS", text=len(self._csrp_impressions))
        self._output_controller.log_info(info_type="TOTAL_RESPONSES_EXAMINED", text=len(self._responses_examined))
        return return_string

    def get_last_action(self):
        """
        Returns the last action performed by the simulated user.
        If no previous action is present, None is returned - this is only true at the start of a simulated search session.
        """
        if self._actions:
            last_action = self._actions[-1]
        else:
            last_action = Actions.START
        
        return last_action
    
    def set_action(self, action):
        """
        This method is key - depending on the action that is passed to it, the relevant method handling the tidying up for that action is called.
        This is the publicly exposed method for recording doing some action.
        """
        if self.action_mappings[action]:
            self._actions.append(action)
            self.action_mappings[action]()
    
    def _set_query_action(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _set_serp_action(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def _set_utterance_action(self):
        pass

    def _set_csrp_action(self):
        """
        Method called when a Conversational SERP is initially examined.
        Any modifications to the search context can be undertaken here.
        """
        self._csrp_impressions.append(self._current_csrp_impression)
        
    
    def _set_snippet_action(self):
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
        
    def _set_response_action(self):
        """
        Method called when a response is examined.
        Any modifications to the search context can be undertaken here.
        """
        self._responses_examined.append(self._current_response)
        

    def _set_mark_response_action(self):
        """
        Called when the currently examined response is to be marked as relevant.
        """
        pass
    
    def _set_stop_action(self):
        """
        Called when the simulated user wishes to stop.
        """
        pass 

    def add_issued_utterance(self, utterance_text):
        """
        Adds a utterance to the stack of previously issued queries.
        """
        self._issued_utterances.append(utterance_text)
        self._last_utterance = utterance_text
    
    def get_last_utterance(self):
        """
        Returns the latest utterance to be issued.
        If no prior utterance has been issued, then None is returned.
        """
        if len(self._issued_utterances) == 0:
            return None
        
        return self._issued_utterances[-1]  # Return the last element in the list (the latest item)
    
    
    def get_last_utterance(self):
        """
        Returns the previous utterance issued. 
        If no previous utterance has been issued, None is returned.
        """
        return self._last_utterance
    
    def get_topic(self):
        """
        Returns the topic Document object.
        """
        return self.topic
    
        
    def get_all_examined_responses(self):
        """
        Returns a list of Document objects representing all of the documents examined by the simulated agent
        over the ENTIRE SEARCH SESSION.
        The most recent document examined is the last document in the list - i.e. examined documents are listed in chronological order.
        An empty list indicates that no documents have been examined for the current query.
        """
        return self._responses_examined
    
    def get_issued_utterances(self):
        """
        Returns a list of all utterances that have been issued for the given search session.
        """
        return self._issued_utterances
    
    def add_irrelevant_response(self, response):
        pass

    def add_relevant_response(self, response):
        pass

    def get_current_response(self):
        return None
    
    def add_csrp_impression(self, is_attractive):
        if is_attractive:
            self._attractive_csrp_count += 1
        else:
            self._unattractive_csrp_count += 1


    def get_last_response(self):
        return self._last_response
    
    def get_current_response():
        
        return None
    
