import abc
import logging
import random

log = logging.getLogger('utterance_generators.base_generator')

class BaseUtteranceGenerator(object):
    """
    The base Utterance generator class.
    You can use this to inherit from to make your own query generator
    """
    def __init__(self):
        self._utterance_list = [
            'What is information retrieval?',
            'What is a search engine?',
            'What is a conversational agent?',
        ]

    def generate_utterance_list(self, user_context):
        """
        Given a Topic object, produces a list of query terms that could be issued by the simulated agent.
        """
        topic = user_context.topic
        topic_text = "{0} {1}".format(topic.title, topic.content)
        # does not currently generate and utterances just returns a fixed list
        return self._utterance_list

    def update_model(self, user_context):
        """
        Enables the model of query/topic to be updated, based on the search context
        The update model based on the documents etc in the search context (i.e. memory of the user)

        :param  user_context: user_contexts.user_context object
        :return: returns True is topic model is updated.
        """
        return False

    def get_next_utterance(self, user_context):
        """
        Returns the next query - if one that hasn't been issued before is present.
        """
        if self._utterance_list is None:
            self._utterance_list = self.generate_utterance_list(user_context)
        
        if user_context.utterance_limit > 0:  # If query_limit is a positive integer, a query limit is enforced. So check the length.
            number_utterances = len(user_context.get_issued_utterances())
            
            if number_utterances == user_context.utterance_limit:  # If this condition is met, no more uttterances may be issued.
                return None
        
        issued_utterance_list = user_context.get_issued_utterances()
        
        # randomly select a utterances from the self._utterance_list
        # randomly select an item from the list
        candidate_utterance = random.choice(self._utterance_list)

        return candidate_utterance
            