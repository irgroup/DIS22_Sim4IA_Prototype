from simiir.utils.config_readers.base_config_reader import BaseConfigReader
from simiir.utils.config_readers import empty_string_check, check_attributes
from simiir.utils.config_readers.component_generators.conversation_user_generator import ConversationUserComponentGenerator

class ConversationalUserConfigReader(BaseConfigReader):
    """
    The User Configuration reader - checks for valid settings, and creates a series of components to represent the given configuration.
    """
    user_type = 'ConversationalSearchUser'

    def __init__(self, config_filename=None):
        super(ConversationalUserConfigReader, self).__init__(config_filename=config_filename, dtd_filename='conversational_user.dtd')
    
    def get_component_generator(self, simulation_components):
        """
        Returns a component generator for the given user configuration.
        """
        return ConversationUserComponentGenerator(simulation_components, self._config_dict)
    
    def _validate_config(self):
        """
        Validates the contents of the configuration file - under the assumption that it is well formed and conforms to the DTD.
        Checks aspects such as the types of attributes, for example.
        """
        # User ID
        empty_string_check(self._config_dict['@id'])

        # Utterance Generators
        empty_string_check(self._config_dict['utteranceGenerator']['@class'])
        check_attributes(self._config_dict['utteranceGenerator'])

        # CSRP Impressions
        empty_string_check(self._config_dict['csrpImpression']['@class'])
        check_attributes(self._config_dict['csrpImpression'])

        # Response Classifiers
        empty_string_check(self._config_dict['responseClassifier']['@class'])
        check_attributes(self._config_dict['responseClassifier'])

        # Response Decision Makers
        empty_string_check(self._config_dict['responseDecisionMaker']['@class'])
        check_attributes(self._config_dict['responseDecisionMaker'])

        # Search Context
        empty_string_check(self._config_dict['userContext']['@class'])
        check_attributes(self._config_dict['userContext'])

        # Logger
        empty_string_check(self._config_dict['logger']['@class'])
        check_attributes(self._config_dict['logger'])