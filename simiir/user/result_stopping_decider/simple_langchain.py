from simiir.user.loggers import Actions
from simiir.user.result_stopping_decider.base import BaseDecisionMaker
from simiir.user.utils.langchain_wrapper import LangChainWrapper

from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from simiir.utils.tidy import clean_html

import logging

log = logging.getLogger('result_stopping_decider.simple_langchain')

class SimpleLangChainDecisionMaker(BaseDecisionMaker):
    """
    A concrete implementation of a decision maker.
    Uses an LLM to decide whether to review the new snippet or issue a new query given previously examined snippets.
    """
    def __init__(self, user_context, logger, prompt_file,provider = 'ollama', model = 'mistral', temperature = 0.0, verbose = False):
        super(SimpleLangChainDecisionMaker, self).__init__(user_context, logger)

        prompt_template = ""
        with open(prompt_file,'r') as prompt:
            prompt_template = prompt.read()
        self._template = prompt_template + """\n\n{format_instructions}\n"""
        log.debug(self._template)

        self._result_schema = [ResponseSchema(
            name="action",
            description=f"Return \"Snippet\" if you should review the next snippet. Return \"Query\" if this search should be abandoned and a new query issued.",
            type="string"
            )]
        
        self._output_parser = StructuredOutputParser.from_response_schemas(self._result_schema)

        format_instructions = self._output_parser.get_format_instructions()
        log.debug(f'init(): {format_instructions}')
        self._prompt = PromptTemplate(
            template=self._template,
            input_variables=["topic_title", "topic_description","viewed_snippets","current_snippet"],
            partial_variables={"format_instructions": format_instructions})
        
        self._llm = LangChainWrapper(self._prompt, provider, model, temperature, verbose)
    
    def decide(self):
        """
        Have the LLM decide if the snippet should be viewed or a new query issued.
        """
        topic_title = self._user_context.topic.title
        topic_description  = self._user_context.topic.content

        examined_snippets = self._user_context.get_examined_snippets()[:-1]
        snippet_text = []
        for snippet in examined_snippets:
            snip = "Title:{0}\nContent:{1}\n".format(snippet.title," ".join(clean_html(snippet.content)))
            snippet_text.append(snip)
        old_snippets = "=== BEGIN OLD SNIPPETS ===\n\n{0}\n\n=== END OLD SNIPPETS ===".format("\n\n".join(snippet_text))
        
        curr_snippet = self._user_context.get_current_snippet()
        new_snippet = "=== BEGIN NEW SNIPPET ===\nTitle: {0}\nContent:{1}\n=== END NEW SNIPPET ===".format(curr_snippet.title," ".join(clean_html(curr_snippet.content)))

        log.debug('decide(before): ' + self._prompt.format(topic_title=topic_title, topic_description=topic_description,current_snippet=new_snippet,viewed_snippets=old_snippets))    
        out = self._llm.generate_response(self._output_parser,{ 'topic_title': topic_title, 'topic_description': topic_description, 'current_snippet': new_snippet, 'viewed_snippets': old_snippets},self._result_schema)
        log.debug(f'decide(after): {out}')

        if out['action'] == "Query":
            return Actions.QUERY
        else:
            return Actions.SNIPPET