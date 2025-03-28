import os
from simiir.utils.config_readers.component_generators.base_generator import BaseComponentGenerator

class ConversationUserComponentGenerator(BaseComponentGenerator):
    """
    """
    def __init__(self, simulation_components, config_dict):
        super(ConversationUserComponentGenerator, self).__init__(config_dict)
        
        self.__simulation_components = simulation_components
        
        
        # Store the user's ID for easy access.
        self.id = self._config_dict['@id']
        self.type = self._config_dict['@type']

        self.user_context = self._get_object_reference(config_details=self._config_dict['userContext'],
                                                         package='user.contexts',
                                                         components=[('search_interface', self.__simulation_components.search_interface),
                                                                     ('output_controller', self.__simulation_components.output),
                                                                     ('topic', self.__simulation_components.topic),
                                                                    ])

        self.logger = self._get_object_reference(config_details=self._config_dict['logger'],
                                                         package='user.loggers',
                                                         components=[('output_controller', self.__simulation_components.output),
                                                                     ('user_context', self.user_context)])

        self.utterance_generator = self._get_object_reference(config_details=self._config_dict['utteranceGenerator'],
                                                              package='user.utterance_generators',
                                                              components=[])
        
        self.csrp_impression = self._get_object_reference(config_details=self._config_dict['csrpImpression'],
                                                          package='user.csrp_impression',
                                                          components=[('user_context', self.user_context)])
        
        self.response_classifier = self._get_object_reference(config_details=self._config_dict['responseClassifier'],
                                                              package='user.response_classifiers',
                                                              components=[('topic', self.__simulation_components.topic),
                                                                          ('user_context', self.user_context)])
        
        self.response_decision_maker = self._get_object_reference(config_details=self._config_dict['responseDecisionMaker'],
                                                                 package='user.response_stopping_deciders',
                                                                 components=[('user_context', self.user_context),
                                                                             ('logger', self.logger)])

    
    def prettify(self):
        """
        Returns a prettified string representation with the key configuration details for the simulation.
        """
        return_string = "{0}**Conversational Search User**{1}".format(" "*self.__simulation_components.output.output_indentation*2, os.linesep)
        return_string = "{0}{1}{2}".format(return_string, "{0}User Context: {1}{2}{3}".format(" "*self.__simulation_components.output.output_indentation*2, self._config_dict['userContext']['@class'], os.linesep, self._prettify_attributes(self._config_dict['userContext'], self.__simulation_components.output.output_indentation)), os.linesep)
        return_string = "{0}{1}{2}".format(return_string, "{0}Utterance Generator: {1}{2}{3}".format(" "*self.__simulation_components.output.output_indentation*2, self._config_dict['utteranceGenerator']['@class'], os.linesep, self._prettify_attributes(self._config_dict['utteranceGenerator'], self.__simulation_components.output.output_indentation)), os.linesep)
        return_string = "{0}{1}{2}".format(return_string, "{0}CSRP Impression: {1}{2}{3}".format(" "*self.__simulation_components.output.output_indentation*2, self._config_dict['csrpImpression']['@class'], os.linesep, self._prettify_attributes(self._config_dict['csrpImpression'], self.__simulation_components.output.output_indentation)), os.linesep)
        return_string = "{0}{1}{2}".format(return_string, "{0}Response Classifier: {1}{2}{3}".format(" "*self.__simulation_components.output.output_indentation*2, self._config_dict['responseClassifier']['@class'], os.linesep, self._prettify_attributes(self._config_dict['responseClassifier'], self.__simulation_components.output.output_indentation)), os.linesep)
        return_string = "{0}{1}{2}".format(return_string, "{0}Response Decision Maker: {1}{2}{3}".format(" "*self.__simulation_components.output.output_indentation*2, self._config_dict['responseDecisionMaker']['@class'], os.linesep, self._prettify_attributes(self._config_dict['responseDecisionMaker'], self.__simulation_components.output.output_indentation)), os.linesep)
        
        return return_string

   