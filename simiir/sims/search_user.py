import os
import pickle
from user.loggers import Actions
from ifind.search.query import Query
from sims.base import SimulatedBaseUser

class SimulatedUser(SimulatedBaseUser):
    """
    The simulated user. Stores references to all the required components, and contains the logical workflow for the simulation.
    """
    def __init__(self, configuration):
        # call the parent class constructor
        super(SimulatedUser, self).__init__(configuration)
        
        self._query_generator = configuration.user.query_generator
        self._serp_impression = configuration.user.serp_impression
        self._snippet_classifier = configuration.user.snippet_classifier
        self._document_classifier = configuration.user.document_classifier
        self._result_stopping_decision_maker = configuration.user.decision_maker
        """
        The workflow implemented below is as follows. Steps with asterisks are DECISION POINTS.
        
        (1)  User issues query
        (2)  User looks at the SERP
        (3*) If the SERP looks poor, goto (1) else goto (4)
        
        (4)  Examine a snippet
        (5*) If the snippet looks at least somewhat relevant, goto (6) else decide whether to goto (1) or (4)
        
        (6)  Examine document
        (7*) If the document looks to be relevant to the provided topic, goto (8), else decide whether to goto (1) or (4)
        
        (8)  Mark the document
        (9*) Decide whether to goto (1) or (4)
        """
       
    
    def _do_query(self):
        """
        Called when the simulated user wishes to issue another query.
        This works by calling the search context for the subsequent query text, and is then issued to the search interface by the search context on behalf of the user.
        If no further queries are available, the logger is told of this - and the simulation will then stop at the next iteration.
        """
        # update the query generator with the latest search context.
        self._query_generator.update_model(self._user_context)

        # Get a query from the generator.
        query_text = self._query_generator.get_next_query(self._user_context)
        
        if query_text:
            self._user_context.add_issued_query(query_text)  # Can also supply page number and page lengths here.
            self._logger.log_action(Actions.QUERY, query=query_text)
            self._output_controller.log_query(query_text)
            
            return True
        
        self._output_controller.log_info(info_type="OUT_OF_QUERIES")
        # Tells the logger that there are no remaining queries; the logger will then stop the simulation.
        self._logger.queries_exhausted()
        return False
    
    def _do_serp(self):
        """
        Called when the simulated user wishes to examine a SERP - the "initial glance" - after issuing a query.
        If the SERP has no results, we continue with the next action - otherwise we will always go and look at said SERP.
        """
        if self._user_context.get_current_results_length() == 0:
            self._logger.log_action(Actions.SERP, status="EMPTY_SERP")
            return False  # No results present; return False (we don't continue with this SERP)
        
        # Code updates on 2017-09-28 for refactoring.
        # Simplified this portion -- the SERP impression component now only returns a True/False value.
        is_serp_attractive = self._serp_impression.is_serp_attractive()
        self._user_context.add_serp_impression(is_serp_attractive)  # Update the search context.
        
        if is_serp_attractive:
            self._logger.log_action(Actions.SERP, status="EXAMINE_SERP")
        else:
            self._logger.log_action(Actions.SERP, status="IGNORE_SERP")
        
        return is_serp_attractive
    
    
    def _do_snippet(self):
        """
        Called when the user needs to make the decision whether to examine a snippet or not.
        The logic within this method supports previous observations of the same document, and whether the text within the snippet appears to be relevant.
        """
        judgment = False
        snippet = self._user_context.get_current_snippet()
        self._user_context.increment_serp_position()
        
        if self._user_context.get_document_observation_count(snippet) > 0:
            # This document has been previously seen; so we ignore it. But the higher the count, cumulated credibility could force us to examine it?
            self._logger.log_action(Actions.SNIPPET, status="SEEN_PREVIOUSLY", snippet=snippet)
        
        else:
            # This snippet has not been previously seen; check quality of snippet. Does it show some form of relevance?
            # If so, we return True - and if not, we return False, which moves the simulator to the next step.
            
            #print 'snippet', snippet.doc_id, self._snippet_classifier.is_relevant(snippet)
            
            if self._snippet_classifier.is_relevant(snippet):
                snippet.judgment = 1
                self._logger.log_action(Actions.SNIPPET, status="SNIPPET_RELEVANT", snippet=snippet)
                judgment = True
            else:
                snippet.judgment = 0
                self._logger.log_action(Actions.SNIPPET, status="SNIPPET_NOT_RELEVANT", snippet=snippet)
        
            self._snippet_classifier.update_model(self._user_context)
        return judgment
    
    def _do_assess_document(self):
        """
        Called when a document is to be assessed.
        """
        judgment = False
        if self._user_context.get_last_query():
            document = self._user_context.get_current_document()
            self._logger.log_action(Actions.DOC, status="EXAMINING_DOCUMENT", doc_id=document.doc_id)
        
            if self._document_classifier.is_relevant(document):
                document.judgment = 1
                #self._logger.log_action(Actions.MARK, status="CONSIDERED_RELEVANT", doc_id=document.doc_id)
                self._user_context.add_relevant_document(document)
                judgment = True
            else:
                document.judgment = 0
                self._user_context.add_irrelevant_document(document)
                #self._logger.log_action(Actions.MARK, status="CONSIDERED_NOT_RELEVANT", doc_id=document.doc_id)
                judgment = False

            self._document_classifier.update_model(self._user_context)
        
        return judgment
    
    def _do_mark_document(self):
        """
        The outcome of marking a document as relevant. At this stage, the user has decided that the document is relevant; hence True can be the only result.
        """
        judgement_message = {0: 'CONSIDERED_NOT_RELEVANT', 1: 'CONSIDERED_RELEVANT'}
        document = self._user_context.get_current_document()
        self._logger.log_action(Actions.MARK, status=judgement_message[document.judgment], doc_id=document.doc_id)
        return True
    
    def _do_result_stopping_decider(self):
        """
        Method which returns whether a further snippet should be examined, the next query should be issued, or some other action.
        This is the "decision making" logic - and is abstracted to the instantiated DecisionMaker instance to work this out.
        """
        current_serp_length = self._user_context.get_current_results_length()
        current_serp_position = self._user_context.get_current_serp_position() + 1
        
        if current_serp_position > current_serp_length:
            # If this condition arises, we have reached the end of the SERP!
            # When SERP pagination is implemented, this condition will either result in moving to the next SERP page or query.
            self._output_controller.log_info(info_type="SERP_END_REACHED")
            return Actions.QUERY
        
        return self._result_stopping_decision_maker.decide()
    
    def _after_query(self):
        self._do_action(Actions.SERP)

    def _after_serp(self):
        if self._action_value:
            self._do_action(Actions.SNIPPET)
        else:
            self._do_action(Actions.QUERY)            

    def _after_snippet(self):
        if self._action_value:
            self._do_action(Actions.DOC)
        else:
            self._do_action(self._do_result_stopping_decider())

    def _after_assess_document(self):
        if self._action_value:
            self._do_action(Actions.MARK)
        else:
            self._do_action(self._do_result_stopping_decider())

    def _after_mark(self):
        #This condition will always be True; we won't get here unless the document has been successfully marked!
        #After the document has been marked, the user must decide whether (s)he wants to look at the subsequent snippet, or issue another query.
        self._do_action(self._do_result_stopping_decider())
    
    def _after_none(self):
        """
        If no action has been supplied from before, then we must be at the start of the search session.
        Therefore, we begin by querying.
        """
        self._do_action(Actions.QUERY)
