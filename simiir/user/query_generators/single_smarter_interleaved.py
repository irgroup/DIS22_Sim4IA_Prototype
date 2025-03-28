from ifind.common.query_ranker import QueryRanker
from ifind.common.query_generation import SingleQueryGeneration
from simiir.user.query_generators.base import BaseQueryGenerator

from simiir.user.query_generators.single_term import SingleTermQueryGenerator
from simiir.user.query_generators.smarter import SmarterQueryGenerator

class SingleSmarterInterleavedQueryGenerator(BaseQueryGenerator):
    """
    Takes the SingleTermGenerator and the SmarterQueryGenerator, and interleaves like [Single,Smarter,Single,Smarter,Single,Smarter...]
    """
    def __init__(self, stopword_file, background_file=[], reverse_single=False):
        super(SingleSmarterInterleavedQueryGenerator, self).__init__(stopword_file, background_file=background_file)
        self.__single = SingleTermQueryGenerator( stopword_file, background_file)
        self.__smarter = SmarterQueryGenerator(stopword_file, background_file)
        self.__reverse_single = reverse_single

    def generate_query_list(self, user_context):
        """
        Given a Topic object, produces a list of query terms that could be issued by the simulated agent.
        """

        topic = user_context.topic

        single_queries = self.__single.generate_query_list(user_context)
        
        if self.__reverse_single:
            single_queries.reverse()
        
        smarter_queries = self.__smarter.generate_query_list(user_context)
        
        interleaved_queries = [val for pair in zip(single_queries, smarter_queries) for val in pair]
        
        return interleaved_queries