from simiir.utils.config_readers.base_config_reader import BaseConfigReader
from simiir.utils.config_readers import empty_string_check, check_attributes
from simiir.utils.config_readers.component_generators.search_user_generator import SearchUserComponentGenerator

class SearchUserConfigReader(BaseConfigReader):
    """
    The User Configuration reader - checks for valid settings, and creates a series of components to represent the given configuration.
    """
    user_type = 'SearchUser'
    
    def __init__(self, config_filename=None):
        super(SearchUserConfigReader, self).__init__(config_filename=config_filename, dtd_filename='search_user.dtd')
    
    def get_component_generator(self, simulation_components):
        """
        Returns a component generator for the given user configuration.
        """
        return SearchUserComponentGenerator(simulation_components, self._config_dict)
    
    def _validate_config(self):
        """
        Validates the contents of the configuration file - under the assumption that it is well formed and conforms to the DTD.
        Checks aspects such as the types of attributes, for example.
        """
        # User ID
        empty_string_check(self._config_dict['@id'])
  
        # Query Generator
        empty_string_check(self._config_dict['queryGenerator']['@class'])
        check_attributes(self._config_dict['queryGenerator'])
        
        # Snippet Classifier
        empty_string_check(self._config_dict['textClassifiers']['snippetClassifier']['@class'])
        check_attributes(self._config_dict['textClassifiers']['snippetClassifier'])
        
        # Document Classifier
        empty_string_check(self._config_dict['textClassifiers']['documentClassifier']['@class'])
        check_attributes(self._config_dict['textClassifiers']['documentClassifier'])
        
        # Stopping Decision Maker
        empty_string_check(self._config_dict['stoppingDecisionMaker']['@class'])
        check_attributes(self._config_dict['stoppingDecisionMaker'])
        
        # Logger
        empty_string_check(self._config_dict['logger']['@class'])
        check_attributes(self._config_dict['logger'])
        
        # Search Context
        empty_string_check(self._config_dict['userContext']['@class'])
        check_attributes(self._config_dict['userContext'])
        
        # SERP Impression
        empty_string_check(self._config_dict['serpImpression']['@class'])
        check_attributes(self._config_dict['serpImpression'])