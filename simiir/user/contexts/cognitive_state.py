from simiir.user.contexts.memory import Memory

class CognitiveState(Memory):
    """
        The Cognitive States of the simulated search user.
        We assume the cognitive state is a immediate reflection of users' preferences and intentions.
        The preferences and intentions are based on the user's past interactions that stored in the memory.
    """
    def __init__(self, search_interface, output_controller, topic):
        
        self.topic_preferences = []
        self.current_certainty_level = None 
        self.current_sentiment_level = None

    def get_historical_interactions(self):
        self._all_documents_examined = self.get_all_documents_examined()
        self._all_snippets_examined = self.get_all_snippets_examined()
        self._issued_queries = self.get_issued_queries()

    def get_topic_preferences(self):
        """
            Returns the topic preferences of the user according to the historical interactions.
        """
        # raise a not implemented error
        raise NotImplementedError("Method not implemented")
    
    def set_certainty_level(self, certainty_level):
        """
        Sets the current certainty level of search and query formulation.
        Certainty level can be used to 
        1. determine the level of confidence in the user's preferences and intentions.
        2. determine the level of confidence in the user's search and query formulation.
        3. determine the depth of search and turns of interactions.

        Reference:

        Moshfeghi, Yashar, and Joemon M. Jose. "On cognition, emotion, and interaction 
        aspects of search tasks with different search intentions." In Proceedings of the 
        22nd international conference on World Wide Web, pp. 931-942. 2013.
        """
        assert certainty_level >= 0.0 and certainty_level <= 1.0
        self.current_certainty_level = certainty_level

    def get_certainty_level(self):
        """
            Returns the current certainty level of search and query formulation.
        """
        if self.current_certainty_level is None:
            raise ValueError("Certainty level has not been set.")
        return self.current_certainty_level
    
    def set_sentiment_level(self, sentiment_level):
        """
        Sets the current sentiment level of the user.
        Sentiment level can be used to 
        1. determine the user's intent of interacting with search results in the same polarity.

        The sentiment level ranges from 0.0 to 1.0.
        The sentiment is likely to be positive if the sentiment level is close to 1.0 
        and to be negative if the sentiment level is close to 0.0.

        Reference:

        Landoni, Monica, Maria Soledad Pera, Emiliana Murgia, and Theo Huibers. "Inside out: 
        Exploring the emotional side of search engines in the classroom." In Proceedings of 
        the 28th ACM conference on user modeling, adaptation and personalization, pp. 136-144. 2020.
        """
        assert sentiment_level >= 0.0 and sentiment_level <= 1.0
        self.current_sentiment_level = sentiment_level

    def get_sentiment_level(self):
        """
            Returns the current sentiment level of the user.
        """
        if self.current_sentiment_level is None:
            raise ValueError("Sentiment level has not been set.")
        return self.current_sentiment_level