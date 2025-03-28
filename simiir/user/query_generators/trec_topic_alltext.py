__author__ = 'leif'

from simiir.user.query_generators.base import BaseQueryGenerator

class TrecTopicAllTextQueryGenerator(BaseQueryGenerator):
    """
    TREC topic title and description Query - only generates one query from the topic title and description.
    """
    
    def generate_query_list(self, user_context):
        """
        Given a Topic object, produces a list of query terms that could be issued by the simulated agent.
        """
        topic = user_context.topic
        return [ (topic.get_topic_text_nopunctuation(), 1) ]
