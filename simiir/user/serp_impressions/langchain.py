#Authors: Adam Roegiest
#Date:   2024-04-20

from simiir.user.serp_impressions.base import BaseSERPImpression
from simiir.user.utils.langchain_wrapper import LangChainWrapper
from simiir.utils.tidy import clean_html

from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

import logging

log = logging.getLogger('serp_impressions.langchain')

class LangChainSERPImpression(BaseSERPImpression):
    """
    An implementation of the SERP impression component that uses an LLM to judge the SERP.
    The LLM is prompted to ask whether the user should examine the SERP or not based upon
    the snippets present.
    """
    def __init__(self, user_context, qrel_file, prompt_file, host=None, port=None,provider="ollama",model="mistral",temperature=0.0,verbose=False):
        super(LangChainSERPImpression,self).__init__(user_context,qrel_file,host,port)
        prompt_template = ""
        with open(prompt_file,'r') as prompt:
            prompt_template = prompt.read()
        self._template = prompt_template + """\n\n{format_instructions}\n"""
        log.debug(self._template)
        self._result_schema = [
            ResponseSchema(
                name="view",
                description="Respond with True if you believe you should examine the current search engine page and False otherwise.",
                type="boolean"
            ),
            ResponseSchema(
                name="explain",
                description="Explain why you believe you should or should not examine the SERP.",
                type="string"
            )]

        self._output_parser = StructuredOutputParser.from_response_schemas(self._result_schema)

        format_instructions = self._output_parser.get_format_instructions(only_json=True)
        log.debug(f'init(): {format_instructions}')
     
        self._prompt = PromptTemplate(
            template=self._template,
            input_variables=["topic_title", "topic_description","old_relevant_snippets","new_snippets"],
            partial_variables={"format_instructions": format_instructions})
    
        self._llm = LangChainWrapper(self._prompt,provider,model,temperature,verbose)

    def is_serp_attractive(self):
        topic = self._user_context.topic.title
        description = self._user_context.topic.content
        results_len = self._user_context.get_current_results_length()
        results_list = self._user_context.get_current_results()
        goto_depth = self.viewport_size
        
        if results_len < goto_depth:  # Sanity check -- what if the number of results is super small?
            goto_depth = results_len

        # Get old examined snippets. In theory, we may want to limit this but practically it may not matter
        # if we only consider "relevant" ones.
        snippet_list = self._user_context.get_all_examined_snippets()
        old_relevant_snippets = []
        for snippet in snippet_list:
            if snippet.judgment > 0:
                snippet ='=====Snippet: {0}======\n{2}\n=========\n'.format(snippet.title," ".join(clean_html(snippet.content)))
                old_relevant_snippets.append(snippet)
        old_relevant_snippets = '\n'.join(old_relevant_snippets)

        # Get the snippets from the SERP. 
        # Note that results_list[i].content refers to the whole document and not the SERP
        new_snippets = []
        for i in range(0, goto_depth):
            snippet = "======Snippet {0}:{1}=======\n{2}\n==========\n".format(i,results_list[i].title," ".join(clean_html(results_list[i].summary)))
            new_snippets.append(snippet)
        new_snippets = '\n'.join(new_snippets)


        log.debug('is_serp_attractive(before): ' + self._prompt.format(topic_title=topic,topic_description=description,old_relevant_snippets=old_relevant_snippets,new_snippets=new_snippets))
        out = self._llm.generate_response(self._output_parser,{'topic_title':topic,'topic_description':description,'old_relevant_snippets':old_relevant_snippets,'new_snippets':new_snippets},self._result_schema)
        log.debug(f'is_serp_attractive(after): {out}')
        return out['view']
