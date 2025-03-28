__author__ = 'leif'

from ifind.seeker.trec_qrel_handler import TrecQrelHandler
from simiir.user.result_classifiers.base_informed_trec import BaseInformedTrecTextClassifier

import logging

log = logging.getLogger('informed_trec_classifer.InformedTrecTextClassifier')

class InformedTrecTextClassifier(BaseInformedTrecTextClassifier):
    """
    A concrete implementation of BaseInformedTrecTextClassifier.
    No dice rolling here. What ever is in the judgement file is used.
    """
    def __init__(self, topic, user_context, qrel_file):
        """
        Initialise an instance of the InformedTrecTextClassifier.
        """
        super(InformedTrecTextClassifier, self).__init__(topic, user_context, qrel_file)
        log.debug("Classifier uses TREC qrels to make decision:")
        
        
    def is_relevant(self, document):
        """
        No dice rolling here. Whatever is in the judgement file is used.
        """
        val = self._get_judgment(self._topic.id, document.doc_id)
        log.debug(f'is_relevant(): For topic: {self._topic.id} and Doc: {document.doc_id} the QREL is: {val}')
        if val > 0:
            return True
        else:
            return False
