import abc
from simiir.user.loggers import Actions

class BaseLogger(object):
    """
    An abstract logger class. Contains the skeleton code and abstract methods to implement a full logger.
    Inherit from this class to create a different logger.
    """
    def __init__(self, output_controller, user_context):
        self._output_controller = output_controller
        self._user_context = user_context
        self._queries_exhausted = False
        self._stop = False
        self.action_mapping = {
            Actions.QUERY  : self._log_query,
            Actions.SERP   : self._log_serp,
            Actions.SNIPPET: self._log_snippet,
            Actions.DOC    : self._log_assess,
            Actions.MARK   : self._log_mark_document,
            Actions.UTTERANCE: self._log_utterance,
            Actions.CSRP   : self._log_csrp,
            Actions.RESPONSE: self._log_assess_response,
            Actions.MARKRESPONSE: self._log_mark_response,
            Actions.START: self._log_start,
            Actions.STOP: self._log_stop
        }
    
    def log_action(self, action_name, **kwargs):
        """
        A nice helper method which is publicly exposed for logging an event.
        Import loggers.Actions to use the appropriate event type when determining the action.
        Use additional keywords to provide additional arguments to the logger.
        """
        if self.action_mapping[action_name]:
            self.action_mapping[action_name](**kwargs)
        else:
            self.__log_unknown_action(action_name)
    
    def get_last_query_time(self):
        return 1
    
    def get_last_interaction_time(self):
        return 1
    
    def get_last_marked_time(self):
        return 1
    
    def get_last_relevant_snippet_time(self):
        return 1
    
    def get_progress(self):
        """
        Abstract method. Returns a value between 0 and 1 representing the progress of the simulation.
        0 represents the start of the simulation, and 1 represents total completion (e.g. the user's time limit has elapsed.)
        If the progress of the simulation cannot be determined, return None.
        """
        return None
    
    def start_logging(self):
        self._log_start()
        self._stop = False
    
    
    def is_finished(self):
        """
        Abstract method, only returns indication as to whether the list of queries has been exhausted.
        Extend this method to include additional checks to see if the user has reached the limit to what they can do.
        Depending on the implemented logger, this could be the number of queries issued, a time limit, etc...
        """
        # return if the queries have been exhausted or stop is true
        return self._queries_exhausted or self._stop
    
    def queries_exhausted(self):
        """
        This method is called when the list of queries to be issued has been exhausted.
        Sets an internal flag within the Logger, meaning that the next call to .is_finished() will stop the process.
        """
        self._queries_exhausted = True
    
    def _report(self, action, **kwargs):
        """
        A simple method to report the current action being logged.
        Extend this method and call the parent implementation (via super()) to include additional details.
        """
        return "ACTION {0} ".format(action)
    
    def _log_query(self, **kwargs):
        """
        Abstract method. When inheriting from this class, implement this method to appropriately handle a query event.
        Returns None.
        """
        pass
    
    def _log_serp(self, **kwargs):
        """
        Abstract method. When inheriting from this class, implement this method to appropriately handle a SERP examination.
        Returns None.
        """
        pass
    
    def _log_snippet(self, **kwargs):
        """
        Abstract method. When inheriting from this class, implement this method to appropriately handle the examination of a snippet.
        Returns None.
        """
        pass
    
    def _log_assess(self, **kwargs):
        """
        Abstract method. When inheriting from this class, implement this method to appropriately handle assessing a document.
        Returns None.
        """
        pass
    
    def _log_mark_document(self, **kwargs):
        """
        Abstract method. When inheriting from this class, implement this method to appropriately handle the costs of marking a document.
        Returns None.
        """
        pass

    def _log_utterance(self, **kwargs):
        """
        Abstract method. When inheriting from this class, implement this method to appropriately handle the costs of utterance.
        Returns None.
        """
        pass

    def _log_csrp(self, **kwargs):
        """
        Abstract method. When inheriting from this class, implement this method to appropriately handle the costs of examining a CSRP.
        Returns None.
        """
        pass

    def _log_assess_response(self, **kwargs):
        """
        Abstract method. When inheriting from this class, implement this method to appropriately handle the costs of assessing a response.
        Returns None.
        """
        pass

    def _log_mark_response(self, **kwargs):
        """
        Abstract method. When inheriting from this class, implement this method to appropriately handle the costs of marking a response.
        Returns None.
        """
        pass

    def _log_stop(self, **kwargs):
        self._stop = True
        self._report(Actions.STOP, **kwargs)

    def _log_start(self, **kwargs):
        self._stop = False
        self._report(Actions.START, **kwargs)
    
    def __log_unknown_action(self, **kwargs):
        self._report(Actions.UNKNOWN, **kwargs)