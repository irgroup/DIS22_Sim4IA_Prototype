import abc

class BaseResponseClassifier(object):
    """
    """
    def __init__(self, topic, user_context): 
        self._topic = topic
        self._user_context = user_context
        self.response_score = 0.0
        self.updating = False
    
    #@abc.abstractmethod
    def is_relevant(self, document):
        """
        Returns True if the given response is relevant.
        This is an abstract method; override this method with an inheriting text classifier.
        """
        return True
    
  
    def update_model(self, user_context):
        """
        Enables the model of relevance/topic to be updated, based on the search context
        The update model based on the documents etc in the search context (i.e. memory of the user)

        :param  user_context: user_contexts.user_context object
        :return: returns True is topic model is updated.
        """
        return False
