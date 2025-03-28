from typing import Any, Optional, Union
import logging
from ifind.search.engine import Engine
from simiir.search.interfaces import Document
from ifind.search.response import Response
from ifind.search.exceptions import EngineConnectionException

log = logging.getLogger('ifind.search.engines.terrier')

class Terrier(Engine):
    def __init__(self, 
                 index_ref : Union[str, Any] = '',
                 wmodel : str = None,
                 controls : dict = None,
                 properties : dict = None,
                 text_field : Optional[str] = 'text', 
                 title_field : Optional[str] = 'title',
                 pipeline : Optional[Any] = None,
                 dataset : str = None,
                 variant : str = 'terrier_stemmed_text',
                 memory : bool = False,
                 **kwargs):
        Engine.__init__(self, **kwargs)
        import pyterrier as pt
        if not pt.started():
            pt.init()
        self.index_ref = index_ref
        self.text_field = text_field
        self.title_field = title_field

        if dataset is not None:
            try:
                self.__index = pt.get_dataset(dataset).get_index(variant=variant)
            except Exception as e:
                msg = "Could not open Terrier index from dataset: " + dataset
                raise EngineConnectionException(self.name, msg, e)
        else:
            try:
                self.__index = pt.IndexFactory.of(index_ref, memory=memory) if isinstance(index_ref, str) else index_ref
            except Exception as e:
                msg = "Could not open Terrier index from: " + str(index_ref)
                raise EngineConnectionException(self.name, msg, e)
            
        self.__reader = self.__index.getMetaIndex()
        if self.__reader is None: log.warning("No reader defined, cannot fetch document text, doing so will result in an error")
        for k in ['docno', text_field]:
            if k not in self.__reader.getKeys():
                log.warning(f"Essential MetaData {k} not found in reader, cannot fetch document text, doing so will result in an error")
                self.__reader = None
        self.__text = pt.text.get_text(self.__index, text_field) if self.__reader else None
                
        if pipeline is not None: self.__engine = pipeline
        elif wmodel is not None: self.__engine = pt.BatchRetrieve(self.__index, wmodel=wmodel, controls=controls, properties=properties)
        else: self.__engine = None
    
    @classmethod
    def from_dataset(cls, 
                     dataset : str, 
                     variant : str = 'terrier_stemmed_text', 
                     pipeline : str = None,
                     wmodel : str = None, 
                     controls : dict = None, 
                     properties : dict = None, 
                     text_field : str = 'body', 
                     memory : bool = False):
        import pyterrier as pt
        if not pt.started():
            pt.init()
        index_ref = pt.get_dataset(dataset).get_index(variant=variant)
        return cls(index_ref, 
                   pipeline=pipeline,
                   wmodel=wmodel, 
                   controls=controls, 
                   properties=properties, 
                   text_field=text_field, 
                   memory=memory)

    def get_document(self, document_id):
        idx = self.__reader.getDocument('docno', document_id)
        content = self.__reader.getItem(self.text_field, int(idx))
        try: title = self.__reader.getItem(self.title_field, int(idx))
        except: title = "NA"

        return Document(id=document_id, content=content, doc_id=document_id, title=title)

    def set_engine(self, engine : Any):
        import pyterrier as pt
        if not pt.started():
            pt.init()
        assert issubclass(pt.Transformer, engine), "Engine must be a PyTerrier Transformer."
        self.__engine = engine
    
    def set_wmodel(self, wmodel : str, controls : dict = None, properties : dict = None):
        import pyterrier as pt
        if not pt.started():
            pt.init()
        self.__engine = pt.BatchRetrieve(self.__index, wmodel=wmodel, controls=controls, properties=properties)

    def __parse_query_terms(self, query):
        if not query.top or query.top < 1:
            query.top = 10

        terms = query.terms
        if isinstance(terms, bytes):
            query.terms = terms.decode('utf-8')
    
    @staticmethod
    def _parse_terrier_response(response, title_field='title', text_field='text'):
        output = Response(response['query'].iloc[0])
        for i in range(len(response)):
            row = response.iloc[i]
            title = getattr(row, title_field, "NA")
            url = getattr(row, 'url', row.docno)
            content = getattr(row, text_field, None) 
            rank = row['rank'] + 1
            docid = row.docno 
            score = row.score
            source = row.source
            output.add_result(title=title, 
                                url=url, 
                                content=content,
                                rank=rank, 
                                docid=docid, 
                                score=score,
                                source=source,
                                whooshid=docid)
        
        output.result_total = len(response)
        return output
    
    def _request(self, query):
        response = None
        pagelen = query.top
        if self.__engine:
            terms = query.terms
            response = self.__engine.search(terms)
            response = response.sort_values('score', ascending=False).head(pagelen)
            if self.__reader: response = self.__text.transform(response)
            response['source'] = self.index_ref
            response = self._parse_terrier_response(response)
        return response

    def _search(self, query):
        """
        Concrete method of Engine's interface method 'search'.
        Performs a search and retrieves the results as an ifind Response.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Query Kwargs:
            top (int): specifies maximum amount of results to return, no minimum guarantee

        Returns:
            ifind Response: object encapulsating a search request's results.

        Raises:
            EngineException

        Usage:
            Private method.

        """
        self.__parse_query_terms(query)
        return self._request(query)


        
      