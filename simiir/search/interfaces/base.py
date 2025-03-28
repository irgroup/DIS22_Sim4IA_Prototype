import abc

class BaseSearchInterface(object):
    """
    An abstract implementation of a search interface that the search context will communicate with.
    Inherit from this abstract class to create a custom search interface.
    """
    def __init__(self):
        self._last_response = None
        self._last_query = None
    
    @abc.abstractmethod
    def issue_query(self, query):
        """
        Abstract method used to issue a query to the underlying search engine of a concrete implementation of a search interface.
        Takes an ifind query object as its only parameter.
        """
        pass
    
    @abc.abstractmethod
    def get_document(self, document_id):
        """
        Abstract method used for retrieving a document from the search engine's document index.
        The parameter document_id may be used to uniquely identify a document (e.g. an ID) within the engine's index.
        """
        pass


class ConversationalBaseInterface(BaseSearchInterface):

    def __init__(self):
        super(ConversationalBaseInterface, self).__init__()
        self._last_response = None
        self._last_query = None

    def issue_query(self, query):
        raise NotImplementedError("Method not implemented")

    def get_document(self, document_id):
        raise NotImplementedError("Method not implemented")
    
    @abc.abstractmethod
    def issue_utterance(self, utterance):
        """
        Abstract method used to issue an utterance to the underlying search engine of a concrete implementation of a search interface.
        Takes an ifind query object as its only parameter.
        """
        pass

    @abc.abstractmethod
    def get_response(self, utterance):
        """
        Abstract method used for retrieving a response from the search engine's response index.
        The parameter response_id may be used to uniquely identify a response (e.g. an ID) within the engine's index.
        """
        pass