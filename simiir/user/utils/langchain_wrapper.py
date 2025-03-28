#Authors: Adam Roegiest and Leif Azzopardi
#Date:   2024-04-05
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama, ChatAnthropic, ChatVertexAI, ChatCohere
from langchain_core.prompts import PromptTemplate

from tenacity import retry,wait_exponential,stop_after_attempt

import logging
log = logging.getLogger('user.utils.LangChainWrapper')

class LangChainWrapper(object):
   """
   Provides a convenient wrapper for interacting with LangChain-based LLMs. 
   In particular, response generation has a built-in retry to attempt to ensure
   that the outputs are formatted correctly.
   """
   def __init__(self,prompt,provider="ollama",model="mistral",temperature=0.0,verbose=False):
      provider = provider.lower()
      if provider == 'openai':
            self._llm = ChatOpenAI(model=model,temperature=temperature,verbose=verbose)
      elif provider == 'ollama':
         self._llm = ChatOllama(model=model,temperature=temperature,verbose=verbose)
      elif provider == 'anthropic':
         self._llm = ChatAnthropic(model=model,temperature=temperature,verbose=verbose)
      elif provider == 'vertexai':
         self._llm = ChatVertexAI(model=model,temperature=temperature,verbose=verbose)
      elif provider == 'cohere':
         self._llm = ChatCohere(model=model,temperature=temperature,verbose=verbose)
      else:
         raise Exception("Unknown provider to LangChainWrapper")
         
      self._prompt = prompt
      self._chain = self._prompt | self._llm

   @retry(wait=wait_exponential(multiplier=1,min=1,max=5), stop=stop_after_attempt(10))
   def generate_response(self, output_parser, params, response_schema):
      """
      Generates a response with a retry mechanism that checks for the correct types and retries with
      attempts at guidance but this is fairly flakey depending on the exact model. 
      """
      def do_retry():
         new_prompt = """The provided response for the following request did not produce the a valid JSON response:
         ---BEGIN REQUEST---
         {0}
         ---END REQUEST---
         
         ---BEGIN RESPONSE---
         {1}
         ---END RESPONSE---
         Update the response to meet the formatting instructions.""".format(self._prompt.template, out)
         new_template = PromptTemplate(
            template=new_prompt,
            input_variables=self._prompt.input_variables,
            partial_variables=self._prompt.partial_variables,
         )
         log.debug("generate_response(): do_retry(): new_template: {0}".format(new_template))
         chain = new_template | self._llm | output_parser
         out = chain.invoke(params)  
         log.debug("generate_response(): do_retry(): retried output: {0}".format(out))
         return out
      
      def valid_schema(output,response_schema):
         type_map = {'boolean' : bool, 'string':str, 'list':list}
         for response in response_schema:
            if response.name not in output or type(out[response.name]) != type_map[response.type]:
               return False
         return True

      full_chain = self._chain | output_parser
      out = full_chain.invoke(params)
      log.debug("generate_response(): initial output: {0}".format(out))

      
      if not valid_schema(out, response_schema):
         out = do_retry()
      
      if not valid_schema(out, response_schema):
         raise Exception("generate_response(): No valid output after retrying")
      
   
      return out
