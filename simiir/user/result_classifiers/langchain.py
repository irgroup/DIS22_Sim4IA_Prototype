#Authors: Adam Roegiest and Leif Azzopardi
#Date:   2024-04-05

from simiir.user.result_classifiers.base import BaseTextClassifier
from simiir.user.utils.langchain_wrapper import LangChainWrapper
from simiir.utils.tidy import clean_html
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

import logging
log = logging.getLogger('result_classifier.LangChainTextClassifier')


snippet_response_schema = [
            ResponseSchema(name="relevant", description="Is this result snippet relevant to the topic? True or False.", type="boolean"),
            ResponseSchema(name="topic", description="Is this result snippet about the subject matter in the topic description? True or False.", type="boolean")
            ]

document_response_schema = [
            ResponseSchema(name="relevant", description="Is this document relevant to the topic? True or False.", type="boolean"),
            ResponseSchema(name="topic", description="Is this document about the subject matter in the topic? True or False.", type="boolean"),
            ResponseSchema(name="explain", description="Summarize the information from the document that is relevant to the topic description and the criteria. Be specific and succint but mention all relevant entities.")
            ]

result_schema_dict = { "SnippetResponse":snippet_response_schema, "DocumentResponse":document_response_schema}

class LangChainTextClassifier(BaseTextClassifier):
    """
    Represents the use of a LangChain-based LLM as a result classifier.
    Functions for both documents and snippets by setting an appropriate result-type.

    Prompts have four available variables to be used: the topic title ({topic_title}), the topic
    description ({topic_description}), the document (or snippet) title ({doc_title}), and 
    the document (or snippet) contents ({doc_content}).
    """
    def __init__(self, topic, user_context, prompt_file, result_type_str, provider = 'ollama', model = 'mistral', temperature = 0.0, verbose = False):
        """

        """
        super(LangChainTextClassifier, self).__init__(topic, user_context)
        self.updating = False
        prompt_template = ""
        with open(prompt_file,'r') as prompt:
            prompt_template = prompt.read()
        self._template = prompt_template + """\n\n{format_instructions}\n"""
        log.debug(self._template)
        
        self._result_schema = result_schema_dict[result_type_str]
        
        self._output_parser = StructuredOutputParser.from_response_schemas(self._result_schema)

        format_instructions = self._output_parser.get_format_instructions()
        log.debug(f'init(): {format_instructions}')
        self._prompt = PromptTemplate(
            template=self._template,
            input_variables=["topic_title", "topic_description", "doc_title", "doc_content"],
            partial_variables={"format_instructions": format_instructions})
        
        self._llm = LangChainWrapper(self._prompt, provider, model, temperature, verbose)

    def is_relevant(self, document):
        """
        """
        doc_title = " ".join(clean_html(document.title))
        doc_content = " ".join(clean_html(document.content))
        topic_title = self._topic.title
        topic_description  = self._topic.content

        log.debug('is_relevant(before): ' + self._prompt.format(topic_title=topic_title, topic_description=topic_description, doc_title=doc_title, doc_content=doc_content))    
        out = self._llm.generate_response(self._output_parser,{ 'topic_title': topic_title, 'topic_description': topic_description, 'doc_title': doc_title, 'doc_content': doc_content },self._result_schema)
        log.debug(f'is_relevant(after): {out}')

        return out['relevant']
