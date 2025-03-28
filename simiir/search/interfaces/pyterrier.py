from simiir.search.interfaces.base import BaseSearchInterface
from ifind.search.engines.terrier import Terrier
from typing import Any, Optional, Union
import logging

log = logging.getLogger('simuser.search.interfaces.pyterrier')

class PyTerrierSearchInterface(BaseSearchInterface):
    """
    Interface for using PyTerrier for BatchRetrieval or Meta Index access

    Parameters:
    index_or_dir : Union[str, Any]
        Reference to PyTerrier Index
    dataset : str
        PyTerrier dataset with pre-built index
    variant : str
        Variant of the dataset index to use
    pipeline : Any
        Reference to pre-built PyTerrier pipeline
    wmodel : str
        Reference to PyTerrier weighting model
    controls : dict
        Controls for the weighting model
    properties : dict
        Properties for the weighting model
    text_field : str
        Field in the index to use as the text field
    title_field : str
        Field in the index to use as the title field
    memory : bool
        Whether to load the index into memory
    """
    def __init__(self, 
                 index_or_dir : Optional[Union[str, Any]] = None, 
                 dataset : Optional[str] = None,
                 variant : Optional[str] = 'terrier_stemmed_text',
                 pipeline : Optional[Any] = None,
                 wmodel : Optional[str] = None, 
                 controls : Optional[dict] = None, 
                 properties : Optional[dict] = None, 
                 text_field : Optional[str] = 'text', 
                 title_field : Optional[str] = 'title',
                 memory : Optional[bool] = False,
                 ):
        assert index_or_dir is not None or dataset is not None, "No index or dataset defined"
        super().__init__()
        self.__engine = Terrier(index_ref=index_or_dir, 
                                dataset=dataset,
                                variant=variant,
                                wmodel=wmodel, 
                                controls=controls, 
                                properties=properties, 
                                text_field=text_field,
                                title_field=title_field,
                                pipeline=pipeline,
                                memory=memory)

    def issue_query(self, query, top=100):
        assert self.__engine is not None, "No engine defined"
        query.top = top
        response = self.__engine.search(query)

        self._last_query = query
        self._last_response = response
        return response

    def get_document(self, document_id):
        return self.__engine.get_document(document_id)

class PyTerrierDenseInterface(PyTerrierSearchInterface):
    """
    Interface for using a Dense Retrieval model with PyTerrier

    Parameters:
    index_or_dir : str or Any
        Reference to PyTerrier FlexIndex
    model_name_or_path : str
        Reference to AutoModel HuggingFace compatible model or path to model
    meta_index : str or Any
        Reference to PyTerrier Index
    dataset : str
        PyTerrier dataset with pre-built index
    variant : str
        Variant of the dataset index to use
    index_text_field : str
        Field in the index to use as the text field
    index_title_field : str
        Field in the index to use as the title field
    memory : bool
        Whether to load the index into memory
    batch_size : int
        Batch size for the model
    text_field : str
        Field for the model to use as the text field
    verbose : bool
        Whether to output verbose logging
    device : str or Any
        Device to use for the model
    """
    def __init__(self, 
                 index_or_dir : Union[str, Any], 
                 model_name_or_path : str, 
                 meta_index : Union[str, Any], 
                 dataset : Optional[str] = None,
                 variant : Optional[str] = 'terrier_stemmed_text',
                 index_text_field : Optional[str] = 'text', 
                 index_title_field : Optional[str] = 'title',
                 memory : Optional[bool] = False, 
                 batch_size : Optional[int] = 32, 
                 text_field : Optional[str] = 'text', 
                 verbose : Optional[bool] = False, 
                 device : Optional[Union[str, Any]] = None 
                 ):
        super().__init__(meta_index, 
                         text_field=index_text_field, 
                         title_field=index_title_field,
                         memory=memory,
                         dataset=dataset,
                         variant=variant)
        from pyterrier_dr import HgfBiEncoder
        if isinstance(index_or_dir, str):
            from pyterrier_dr import NumpyIndex 
            index = NumpyIndex(index_or_dir)
        else: index = index_or_dir

        model = HgfBiEncoder.from_pretrained(model_name_or_path, batch_size=batch_size, text_field=text_field, verbose=verbose, device=device)
        self.__engine = model >> index % 1000
    
    def set_wmodel(self, wmodel : str, controls : dict = None, properties : dict = None):
        raise NotImplementedError("This method is not supported for this class")
    
    @classmethod
    def from_dataset(cls, 
                     index_or_dir : Union[str, Any], 
                     model_name_or_path : str, 
                     dataset : str, # Pyterrier dataset with pre-built index
                     variant : str = 'terrier_stemmed_text', # Variant of the dataset index to use
                     meta_index_text_field : str = 'text', 
                     meta_index_title_field : str = 'title',
                     memory=False, 
                     batch_size=32, 
                     text_field='text', 
                     verbose=False, 
                     device=None):
        import pyterrier as pt
        if not pt.started():
            pt.init()
        meta_index_ref = pt.get_dataset(dataset).get_index(variant=variant)
        return cls(index_or_dir, 
                   model_name_or_path, 
                   meta_index_ref, 
                   index_text_field=meta_index_text_field, 
                   index_title_field=meta_index_title_field,
                   memory=memory, 
                   batch_size=batch_size, 
                   text_field=text_field, 
                   verbose=verbose, 
                   device=device)

class PyterrierReRankerInterface(PyTerrierSearchInterface):
    """
    Interface for using a Dense Retrieval model with PyTerrier for re-ranking

    Parameters:
    model_name_or_path : str
        Reference to AutoModel HuggingFace compatible model or path to model
    dataset : str
        PyTerrier dataset with pre-built index
    variant : str
        Variant of the dataset index to use
    meta_index : str or Any
        Reference to PyTerrier Index
    wmodel : str
        Weighting model to use
    controls : dict
        Controls for the weighting model
    properties : dict
        Properties for the weighting model
    index_text_field : str
        Field in the index to use as the text field
    index_title_field : str
        Field in the index to use as the title field
    memory : bool
        Whether to load the index into memory
    batch_size : int
        Batch size for the model
    text_field : str
        Field for the model to use as the text field
    verbose : bool
        Whether to output verbose logging
    device : None
        Device to use for the model
    rerank_depth : int
        Depth to re-rank to
    """
    def __init__(self, 
                 model_or_path : Union[str, Any], 
                 meta_index : Optional[str] = None, 
                 dataset : Optional[str] = None,
                 variant : Optional[str] = 'terrier_stemmed_text',
                 wmodel : Optional[str] = 'BM25',
                 controls : Optional[dict] = None,
                 properties : Optional[dict] = None,
                 index_text_field : Optional[str] = 'text', 
                 index_title_field : Optional[str] = 'title',
                 memory : Optional[bool] = False, 
                 batch_size : Optional[int] = 32, 
                 text_field : Optional[str] = 'text', 
                 verbose : Optional[bool] = False, 
                 device : Optional[Union[str, Any]] = None,
                 rerank_depth : Optional[int] = 100
                 ):
        super().__init__(meta_index, 
                         dataset=dataset,
                         variant=variant,
                         wmodel=wmodel, 
                         controls=controls, 
                         properties=properties, 
                         text_field=index_text_field, 
                         title_field=index_title_field,
                         memory=memory)
        import pyterrier as pt
        if not pt.started():
            pt.init()
        
        self.rerank_depth = rerank_depth
        self.index_text_field = index_text_field
        self.text_field = text_field

        if isinstance(model_or_path, str):
            log.warning("This class assumes the huggingface model is a Bi-Encoder style encoder, if not, this will fail")
            from pyterrier_dr import HgfBiEncoder
            self.model = HgfBiEncoder.from_pretrained(model_or_path, batch_size=batch_size, text_field=text_field, verbose=verbose, device=device)
        else: self.model = model_or_path
        assert issubclass(pt.Transformer, self.model), "Model must be a PyTerrier object"
        self.__engine = self.__engine % self.rerank_depth >> pt.text.get_text(self.__index, index_text_field) >> self.model

    def set_wmodel(self, wmodel : str, controls : dict = None, properties : dict = None):
        import pyterrier as pt
        if not pt.started():
            pt.init()
        super().set_wmodel(wmodel, controls, properties)
        self.__engine = self.__engine % self.rerank_depth >> pt.text.get_text(self.__index, self.index_text_field) >> self.model

    @classmethod
    def from_dataset(cls, 
                     model_or_path : Union[str, Any], 
                     dataset : str, 
                     variant : str = 'terrier_stemmed_text', 
                     wmodel : str = 'BM25',
                     controls : dict = None,
                     properties : dict = None,
                     meta_index_text_field : str = 'text', 
                     meta_index_title_field : str = 'title',
                     memory=False, 
                     batch_size=32, 
                     text_field='text', 
                     verbose=False, 
                     device=None):
        import pyterrier as pt
        if not pt.started():
            pt.init()
        meta_index_ref = pt.get_dataset(dataset).get_index(variant=variant)
        return cls(model_or_path, 
                   meta_index_ref, 
                   wmodel=wmodel, 
                   controls=controls, 
                   properties=properties, 
                   index_text_field=meta_index_text_field, 
                   index_title_field=meta_index_title_field,
                   memory=memory, 
                   batch_size=batch_size, 
                   text_field=text_field, 
                   verbose=verbose, 
                   device=device)