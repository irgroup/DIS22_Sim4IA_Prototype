from ifind.common.query_ranker import QueryRanker
from ifind.common.query_generation import SingleQueryGeneration
from simiir.user.query_generators.base import BaseQueryGenerator

from simiir.user.query_generators.single_term import SingleTermQueryGenerator
from simiir.user.query_generators.smarter import SmarterQueryGenerator

import random
import string

class DudSmarterInterleavedQueryGenerator(BaseQueryGenerator):
    """
    Takes the SmarterQueryGenerator, and interleaves it with guaranteed dud queries (e.g. [dud, smarter, dud, smarter...])
    Dud queries are generated as random strings, consisting of letters and numbers.
    """
    def __init__(self, stopword_file, background_file=[]):
        super(DudSmarterInterleavedQueryGenerator, self).__init__(stopword_file, background_file=background_file, allow_similar=True)
        self.__smarter = SmarterQueryGenerator(stopword_file, background_file)

    def generate_query_list(self, user_context):
        """
        Given a Topic object, produces a list of query terms that could be issued by the simulated agent.
        """
        topic = user_context.topic
        smarter_queries = self.__smarter.generate_query_list(user_context)
        
        interleaved_queries = []
        
        for query in smarter_queries:
            random_str = u''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            
            interleaved_queries.append((random_str, 0))
            interleaved_queries.append(query)
        
        return interleaved_queries