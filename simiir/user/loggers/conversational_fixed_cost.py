from simiir.user.loggers import Actions
from simiir.user.loggers.base import BaseLogger
import progressbar

class ConversationalFixedCostLogger(BaseLogger):
    """
    A fixed cost logger - where interactions have a different - but constant - cost.
    Not the most realistic way of representing interaction costs, but as a start, it is pretty good.
    Costs can be defined in the constructor - and time_limit is the maximum amount of time a search session can be carried out for.
    A session ends when the accumulated costs reaches (or exceeds) the specified time limit. If a user initiates an activity which pushes them over the limit, they can complete that action - but nothing more.
    """
    def __init__(self,
                 output_controller,
                 user_context,
                 time_limit=120,
                 utterance_cost=10,
                 response_cost=30,
                 csrp_impression_cost=5,
                 mark_response_cost=3):
        """
        Instantiates the BaseLogger class and sets up additional instance variables for the FixedCostLogger.
        Note that this does not enforce the time limit...
        """
        super(ConversationalFixedCostLogger, self).__init__(output_controller, user_context)
        
        #  Series of costs (in seconds) for each interaction that the user can perform; these are fixed.
        self._utterance_cost = utterance_cost
        self._response_cost = response_cost
        self._csrp_impression_cost = csrp_impression_cost
        self._mark_response_cost = mark_response_cost
        
        self._total_time = 0  # An elapsed counter of the number of seconds a user has been interacting for.
        self._time_limit = time_limit  # The maximum time that a user can search for in a session.
        
        self._last_utterance_time = 0  # The last time a query was issued, from the start of the session, measured in seconds.
        self._last_marked_time = 0  # The last time a document was marked, from the start of the session, measured in seconds.
        widgets = [' [',
         progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
         '] ',
           progressbar.Bar('*'),' (',
           progressbar.ETA(), ') ',
          ]

        self._bar = progressbar.ProgressBar(maxval=self._time_limit, widgets=widgets)
        self._bar.start()

    def get_last_interaction_time(self):
        return self._total_time
    
    def get_progress(self):
        """
        Concrete implementation of the abstract get_progress() method.
        Returns a value between 0 and 1 representing how far through the current simulation the user is.
        """
        if self._total_time < self._time_limit:
            self._bar.update(self._total_time)
        
        return self._total_time / float(self._time_limit)
    
    def is_finished(self):
        """
        Concrete implementation of the is_finished() method from the BaseLogger.
        Returns True if the user has reached their search "allowance".
        """
        print(self._user_context.get_last_action())
        if self._user_context.get_last_action() == Actions.STOP:
            return True 

        if self._total_time < self._time_limit:
            self._bar.update(self._total_time)
        # Include the super().is_finished() call to determine if there are any queries left to process.
        return (not (self._total_time < self._time_limit)) or super(ConversationalFixedCostLogger, self).is_finished()
    
    def _report(self, action, **kwargs):
        """
        Re-implementation of the _report() method from BaseLogger.
        Includes additional details in the message such as the total elapsed time, and maximum time available to the user after the action has been processed.
        """
        log_entry_mapper = {
            Actions.START  : "START",
            Actions.STOP   : "STOP",
            Actions.UNKNOWN: "UNKNOWN",
            Actions.UTTERANCE  : kwargs.get('utterance'),
            Actions.CSRP   : kwargs.get('status'),
            Actions.RESPONSE    : "{0}".format(kwargs.get('status')),
            Actions.MARKRESPONSE  : "{0}".format(kwargs.get('status')),
        }
        
        base = super(ConversationalFixedCostLogger, self)._report(action, **kwargs)
        self._output_controller.log("{0}{1} {2} {3}".format(base, self._time_limit, self._total_time, log_entry_mapper[action]))
    
    def _log_utterance(self, **kwargs):
        """
        Concrete implementation for logging an utterance at a fixed cost.
        """
        self._total_time = self._total_time + self._utterance_cost
        self._last_utterance_time = self._total_time
        
        self._report(Actions.UTTERANCE, **kwargs)

    def _log_csrp(self, **kwargs):
        """
        Concrete implementation for logging a CSRP impression at a fixed cost.
        """
        self._total_time = self._total_time + self._csrp_impression_cost
        self._report(Actions.CSRP, **kwargs)

    def _log_assess_response(self, **kwargs):
        """
        Concrete implementation for assessing a response at a fixed cost.
        """
        self._total_time = self._total_time + self._response_cost
        self._report(Actions.RESPONSE, **kwargs)

    def _log_mark_response(self, **kwargs):
        """
        Concrete implementation for marking a response as relevant at a fixed cost.
        """
        self._total_time = self._total_time + self._mark_response_cost
        self._last_marked_time = self._total_time
        
        self._report(Actions.MARKRESPONSE, **kwargs)    

