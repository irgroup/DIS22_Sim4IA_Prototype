import os
from simiir.utils.config_readers.component_generators.base_generator import BaseComponentGenerator

class SearchUserComponentGenerator(BaseComponentGenerator):
    """
    """
    def __init__(self, simulation_components, config_dict):
        super(SearchUserComponentGenerator, self).__init__(config_dict)
        
        self.__simulation_components = simulation_components
        
        # Store the user's ID for easy access.
        self.id = self._config_dict['@id']
        self.type = self._config_dict['@type']

        # Create the user's query generator.
        self.query_generator = self._get_object_reference(config_details=self._config_dict['queryGenerator'],
                                                          package='user.query_generators',
                                                          components=[])
        
        # Create the search context object.
        # self.user_context = self.__generate_user_context()  # When we had only a single search context class.
        self.user_context = self._get_object_reference(config_details=self._config_dict['userContext'],
                                                         package='user.contexts',
                                                         components=[('search_interface', self.__simulation_components.search_interface),
                                                                     ('output_controller', self.__simulation_components.output),
                                                                     ('topic', self.__simulation_components.topic),
                                                                    ])
        
        # Create the user's snippet classifier.
        self.snippet_classifier = self._get_object_reference(config_details=self._config_dict['textClassifiers']['snippetClassifier'],
                                                             package='user.result_classifiers',
                                                             components=[('topic', self.__simulation_components.topic),
                                                                         ('user_context', self.user_context)])
        
        # Create the uer's document classifier.
        self.document_classifier = self._get_object_reference(config_details=self._config_dict['textClassifiers']['documentClassifier'],
                                                              package='user.result_classifiers',
                                                              components=[('topic', self.__simulation_components.topic),
                                                                          ('user_context', self.user_context)])
        
        # Generate the logger object for the simulation.
        self.logger = self._get_object_reference(config_details=self._config_dict['logger'],
                                                         package='user.loggers',
                                                         components=[('output_controller', self.__simulation_components.output),
                                                                     ('user_context', self.user_context)])
        
        # Create the decision maker (judging relevancy).
        self.decision_maker = self._get_object_reference(config_details=self._config_dict['stoppingDecisionMaker'],
                                                         package='user.result_stopping_decider',
                                                         components=[('user_context', self.user_context),
                                                                     ('logger', self.logger)])
        
        # Create the SERP impression component (used for some more advanced stopping models).
        self.serp_impression = self._get_object_reference(config_details=self._config_dict['serpImpression'],
                                                          package='user.serp_impressions',
                                                          components=[('user_context', self.user_context)])
    
    def prettify(self):
        """
        Returns a prettified string representation with the key configuration details for the simulation.
        """
        return_string = "{0}**Search User**{1}".format(" "*self.__simulation_components.output.output_indentation*2, os.linesep)
        return_string = "{0}{1}".format("{0}{1}Query Generator: {2}{3}{4}".format(return_string, " "*self.__simulation_components.output.output_indentation*2, self._config_dict['queryGenerator']['@class'], os.linesep, self._prettify_attributes(self._config_dict['queryGenerator'], self.__simulation_components.output.output_indentation)), os.linesep)
        return_string = "{0}{1}{2}".format(return_string, "{0}Snippet Classifier: {1}{2}{3}".format(" "*self.__simulation_components.output.output_indentation*2, self._config_dict['textClassifiers']['snippetClassifier']['@class'], os.linesep, self._prettify_attributes(self._config_dict['textClassifiers']['snippetClassifier'], self.__simulation_components.output.output_indentation)), os.linesep)
        return_string = "{0}{1}{2}".format(return_string, "{0}Document Classifier: {1}{2}{3}".format(" "*self.__simulation_components.output.output_indentation*2, self._config_dict['textClassifiers']['documentClassifier']['@class'], os.linesep, self._prettify_attributes(self._config_dict['textClassifiers']['documentClassifier'], self.__simulation_components.output.output_indentation)), os.linesep)
        return_string = "{0}{1}{2}".format(return_string, "{0}Stopping Decision Maker: {1}{2}{3}".format(" "*self.__simulation_components.output.output_indentation*2, self._config_dict['stoppingDecisionMaker']['@class'], os.linesep, self._prettify_attributes(self._config_dict['stoppingDecisionMaker'], self.__simulation_components.output.output_indentation)), os.linesep)
        return_string = "{0}{1}{2}".format(return_string, "{0}SERP Impression: {1}{2}{3}".format(" "*self.__simulation_components.output.output_indentation*2, self._config_dict['serpImpression']['@class'], os.linesep, self._prettify_attributes(self._config_dict['serpImpression'], self.__simulation_components.output.output_indentation)), os.linesep)
        return_string = "{0}{1}{2}".format(return_string, "{0}Logger: {1}{2}{3}".format(" "*self.__simulation_components.output.output_indentation*2, self._config_dict['logger']['@class'], os.linesep, self._prettify_attributes(self._config_dict['logger'], self.__simulation_components.output.output_indentation)), os.linesep)
        return_string = "{0}{1}{2}".format(return_string, "{0}User Context: {1}{2}{3}".format(" "*self.__simulation_components.output.output_indentation*2, self._config_dict['userContext']['@class'], os.linesep, self._prettify_attributes(self._config_dict['userContext'], self.__simulation_components.output.output_indentation)), os.linesep)
        
        return return_string

   