import abc
import random

class BaseCSRPImpression(object):
    """
    A base class implementation of the CSRP impression component.
    Contains the abstract signature for the is_serp_attractive() method.
    Rolls a dice and randomly returns True or False.
    90% it will return True, 10% it will return False.
    """
    def __init__(self, user_context):
        self._user_context = user_context
    
    #@abc.abstractmethod
    def is_csrp_attractive(self):
        """
        Abstract method that is used to determine if the SERP should be considered attractive or not.
        This is an abstract method; extend this class and override this abstract definition
        to implement this functionality.
        """

        if random.random() < 0.9:
            return True
        else:
            return False

        #raise NotImplementedError("You cannot call is_serp_attractive() from the base SERP impression class.")